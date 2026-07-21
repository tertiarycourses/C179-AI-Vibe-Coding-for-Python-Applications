# models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    """One card transaction presented for screening."""
    id: int
    card_ref: str
    ts: datetime
    amount: float
    merchant_category: str
    city: str
    lat: float
    lon: float

    @property
    def hour(self) -> int:
        """Hour of day, 0-23 — used by the unusual-hour rule."""
        return self.ts.hour

    @property
    def is_high_risk_category(self) -> bool:
        return self.merchant_category in {"crypto_exchange", "gift_cards", "jewellery"}

    def __repr__(self) -> str:
        return (f"Transaction(id={self.id}, card={self.card_ref}, "
                f"${self.amount:,.2f}, {self.merchant_category}, {self.city})")

