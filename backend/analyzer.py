"""Calls the LLM and returns a validated PricingRecommendation.

Works against free models on OpenRouter that occasionally return JSON in the
`content` field instead of using the tool-calling mechanism — we handle both.
"""
from __future__ import annotations

import os
import time
from typing import Optional

from dotenv import load_dotenv
from openrouter import OpenRouter
from openrouter.errors import TooManyRequestsResponseError
from pydantic import ValidationError

from pricing import PricingInput, PricingRecommendation
from prompts import build_user_message, load_system_prompt

load_dotenv()

MODEL = "openai/gpt-oss-120b:free"
TOOL_NAME = "return_pricing_recommendation"
MAX_ATTEMPTS = 2
RATE_LIMIT_RETRIES = 3


class AnalyzerError(Exception):
    pass


class RateLimitedError(AnalyzerError):
    pass


def _build_tool() -> dict:
    return {
        "type": "function",
        "function": {
            "name": TOOL_NAME,
            "description": (
                "Return the final pricing recommendation as structured data. "
                "You MUST call this tool exactly once. Do not produce text outside this call."
            ),
            "parameters": PricingRecommendation.model_json_schema(),
        },
    }


def _send_with_backoff(client, **kwargs):
    """client.chat.send with exponential backoff on 429."""
    for attempt in range(RATE_LIMIT_RETRIES):
        try:
            return client.chat.send(**kwargs)
        except TooManyRequestsResponseError:
            if attempt == RATE_LIMIT_RETRIES - 1:
                raise RateLimitedError(
                    "Rate limited by the :free model provider. "
                    "Wait ~60 seconds or switch to a paid variant."
                )
            time.sleep(2 ** attempt)  # 1s, 2s


def _strip_code_fences(text: str) -> str:
    """Free models often wrap JSON in ```json ... ``` fences."""
    s = text.strip()
    if not s.startswith("```"):
        return s
    # drop opening fence line
    s = s.split("\n", 1)[1] if "\n" in s else s[3:]
    # drop closing fence
    if s.rstrip().endswith("```"):
        s = s.rstrip()[:-3]
    # drop optional 'json' language hint
    if s.lstrip().lower().startswith("json"):
        s = s.lstrip()[4:]
    return s.strip()


def _extract_recommendation(message) -> Optional[PricingRecommendation]:
    """Try tool_calls first, fall back to JSON in content.

    Returns the validated recommendation, or None if nothing usable was found.
    Re-raises ValidationError if the structure is present but schema-invalid
    (so the outer loop can give the model a correction hint).
    """
    tool_calls = getattr(message, "tool_calls", None) or []
    for call in tool_calls:
        if call.function.name == TOOL_NAME:
            raw = call.function.arguments
            if isinstance(raw, str):
                return PricingRecommendation.model_validate_json(raw)
            return PricingRecommendation.model_validate(raw)

    # Fallback: model returned JSON as text
    content = getattr(message, "content", "") or ""
    cleaned = _strip_code_fences(content)
    if cleaned:
        return PricingRecommendation.model_validate_json(cleaned)

    return None


def analyze(req: PricingInput) -> PricingRecommendation:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your .env file "
            "(e.g. OPENROUTER_API_KEY=sk-or-v1-...)."
        )

    tool = _build_tool()
    messages = [
        {"role": "system", "content": load_system_prompt()},
        {"role": "user", "content": build_user_message(req)},
    ]

    with OpenRouter(api_key=api_key) as client:
        last_error = None

        for attempt in range(MAX_ATTEMPTS):
            response = _send_with_backoff(
                client,
                model=MODEL,
                messages=messages,
                tools=[tool],
                tool_choice="auto",
                max_tokens=2048,
            )
            message = response.choices[0].message

            try:
                result = _extract_recommendation(message)
            except (ValidationError, ValueError) as e:
                last_error = str(e)
                result = None

            if result is not None:
                return result

            if attempt == MAX_ATTEMPTS - 1:
                raise AnalyzerError(
                    f"Model failed to return valid output. "
                    f"Last error: {last_error or 'no tool call and no parseable JSON in content'}"
                )

            # Feed the issue back and retry
            messages.append(
                {"role": "assistant", "content": getattr(message, "content", "") or ""}
            )
            if last_error:
                correction = (
                    f"Your previous output failed validation:\n\n{last_error}\n\n"
                    f"Call `{TOOL_NAME}` again with corrected arguments matching the schema."
                )
            else:
                correction = (
                    f"You did not call `{TOOL_NAME}` and did not return valid JSON. "
                    f"Call the tool now. Do not reply with prose."
                )
            messages.append({"role": "user", "content": correction})

    raise AnalyzerError("Exhausted attempts without returning a valid recommendation.")