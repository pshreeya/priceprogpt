from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()  #Must run before importing analyzer (which reads the API key)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from analyzer import AnalyzerError, RateLimitedError, analyze
from pricing import PricingInput, PricingRecommendation

app = FastAPI(title="Pricing Advisor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=PricingRecommendation)
def analyze_endpoint(req: PricingInput) -> PricingRecommendation:
    """Return a structured pricing recommendation for the given scenario."""
    try:
        return analyze(req)
    except RateLimitedError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except AnalyzerError as e:
        raise HTTPException(status_code=502, detail=str(e))