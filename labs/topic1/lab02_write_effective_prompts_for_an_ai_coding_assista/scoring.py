# scoring.py
def score_transaction(amount: float, is_overseas: bool, hour: int) -> dict:
    """Return a 0-100 risk score for one transaction, with its reasons."""
    if amount < 0:
        raise ValueError("amount must not be negative")
    if not 0 <= hour <= 23:
        raise ValueError("hour must be between 0 and 23")

    HIGH_VALUE = 500.00
    score, reasons = 0, []

    if amount > HIGH_VALUE:
        score += 40
        reasons.append("high value")
    if is_overseas:
        score += 30
        reasons.append("overseas merchant")
    if 1 <= hour <= 5:
        score += 20
        reasons.append("unusual hour")

    return {"score": min(score, 100), "reasons": reasons}

