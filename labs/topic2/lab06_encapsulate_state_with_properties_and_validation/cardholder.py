# cardholder.py
class Cardholder:
    """A card account with a running spend baseline used for anomaly scoring."""

    def __init__(self, card_ref: str, name: str, home_city: str, typical_amount: float):
        if typical_amount <= 0:
            raise ValueError("typical_amount must be positive")
        self.card_ref = card_ref
        self.name = name
        self.home_city = home_city
        self._typical_amount = typical_amount   # leading _ = internal
        self._observed_count = 0

    @property
    def typical_amount(self) -> float:
        """Read-only view of the baseline — callers cannot assign to it."""
        return round(self._typical_amount, 2)

    @property
    def observed_count(self) -> int:
        return self._observed_count

