# validate.py
from errors import ValidationError

VALID_CATEGORIES = {"grocery","fuel","restaurant","electronics","online_gaming",
                    "jewellery","crypto_exchange","gift_cards","pharmacy","transport"}

def validate_txn(record: dict) -> dict:
    """Raise ValidationError on the first problem found."""
    amount = record.get("amount")
    if amount is None:
        raise ValidationError("amount", amount, "is required")
    if not isinstance(amount, (int, float)):
        raise ValidationError("amount", amount, "must be numeric")
    if amount <= 0:
        raise ValidationError("amount", amount, "must be positive")
    if amount > 1_000_000:
        raise ValidationError("amount", amount, "exceeds the maximum single charge")
    cat = record.get("merchant_category")
    if cat not in VALID_CATEGORIES:
        raise ValidationError("merchant_category", cat, "is not a known category")
    return record

