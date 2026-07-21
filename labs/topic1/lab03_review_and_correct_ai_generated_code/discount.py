# discount.py
def apply_discount(price, tier):
    if tier == "gold":
        return price * 0.8
    elif tier == "silver":
        return price * 0.9
    elif tier == "bronze":
        return price * 0.95
    return price

# discount.py
DISCOUNTS = {"gold": 0.20, "silver": 0.10, "bronze": 0.05}

def apply_discount(price: float, tier: str) -> float:
    """Return the price after applying the tier discount."""
    if price < 0:
        raise ValueError("price must not be negative")
    key = (tier or "").strip().lower()
    if key not in DISCOUNTS:
        raise ValueError(f"unknown tier: {tier!r}")
    return round(price * (1 - DISCOUNTS[key]), 2)

