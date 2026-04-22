import os

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "pricing_system.md")


def load_system_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_user_message(req) -> str:
    refs = (
        ", ".join(str(p) for p in req.reference_prices)
        if req.reference_prices
        else "(none provided)"
    )
    notes = req.context_notes.strip() if req.context_notes else "(none)"

    return f"""Analyze this pricing scenario and return a recommendation.

<product_type>{req.product_type.value}</product_type>
<current_price>{req.current_price}</current_price>
<reference_prices>{refs}</reference_prices>
<demand_signal>{req.demand_signal}</demand_signal>
<inventory_remaining>{req.inventory_remaining}</inventory_remaining>
<lead_time_days>{req.lead_time_days}</lead_time_days>
<context_notes>
{notes}
</context_notes>
"""