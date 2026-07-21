# schemas.py
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

CATEGORIES = Literal["grocery","fuel","restaurant","electronics","online_gaming",
                     "jewellery","crypto_exchange","gift_cards","pharmacy","transport"]

class TransactionIn(BaseModel):
    """One transaction submitted for screening."""
    card_ref: str = Field(pattern=r"^CH\d{4}$", description="Cardholder reference")
    ts: datetime
    amount: float = Field(gt=0, le=1_000_000, description="Charge amount in SGD")
    merchant_category: CATEGORIES
    city: str = Field(min_length=2, max_length=64)
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)

    @field_validator("city")
    @classmethod
    def title_case_city(cls, v: str) -> str:
        return v.strip().title()

# schemas.py (add)
class RuleHit(BaseModel):
    rule_name: str
    score: float = Field(ge=0, le=1)
    reason: str

class ScreeningOut(BaseModel):
    """What the screening service returns."""
    card_ref: str
    composite_score: float = Field(ge=0, le=1)
    flagged: bool
    decision: Literal["approve", "review", "decline"]
    hits: list[RuleHit] = []
    errors: list[str] = []

