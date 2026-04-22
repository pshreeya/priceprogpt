from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ProductType(str, Enum):
    HOTEL_ROOM = "hotel_room"
    EVENT_TICKET = "event_ticket"
    SHORT_TERM_RENTAL = "short_term_rental"
    ECOM_ITEM = "ecom_item"


class PricingInput(BaseModel):
    """Inputs for a single pricing decision."""

    product_type: ProductType = Field(..., description="Category of the product")
    current_price: float = Field(..., gt=0, description="Current listed price")
    reference_prices: list[float] = Field(
        default_factory=list,
        description="Competitor or market reference prices",
    )
    demand_signal: float = Field(
        ...,
        ge=0,
        le=1,
        description="Normalized demand pressure, 0 (cold) to 1 (hot)",
    )
    inventory_remaining: int = Field(..., ge=0, description="Units left to sell")
    lead_time_days: int = Field(
        ...,
        ge=0,
        description="Days until inventory expires (perishable) or replenishment cycle (ecom)",
    )
    context_notes: str = Field("", description="Free-form context")

    @field_validator("reference_prices")
    @classmethod
    def _prices_positive(cls, v: list[float]) -> list[float]:
        if not all(p > 0 for p in v):
            raise ValueError("All reference prices must be > 0")
        return v


class PricingRecommendation(BaseModel):
    """Structured output from the pricing strategist."""

    suggested_price: float = Field(..., gt=0, description="Recommended price")
    confidence: float = Field(..., ge=0, le=1, description="Confidence, 0–1")
    rationale: list[str] = Field(
        default_factory=list,
        description="2–4 sentences citing specific inputs",
    )
    risk_flags: list[str] = Field(
        default_factory=list,
        description="2–4 concrete risk scenarios",
    )
    expected_lift_pct: Optional[float] = Field(
        None,
        description="Approx revenue change vs current_price. Null only if undefensible.",
    )