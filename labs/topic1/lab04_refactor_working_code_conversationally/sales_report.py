# sales_report.py
orders = [
    {"id": 1, "region": "North", "amount": 1200.50, "status": "paid"},
    {"id": 2, "region": "South", "amount": 890.00, "status": "paid"},
    {"id": 3, "region": "North", "amount": 450.25, "status": "refunded"},
    {"id": 4, "region": "East",  "amount": 2100.75, "status": "paid"},
    {"id": 5, "region": "South", "amount": 310.00, "status": "pending"},
]

totals = {}
for o in orders:
    if o["status"] == "paid":
        if o["region"] not in totals:
            totals[o["region"]] = 0
        totals[o["region"]] += o["amount"]
for r in sorted(totals):
    print(f"{r}: ${totals[r]:,.2f}")
print(f"TOTAL: ${sum(totals.values()):,.2f}")

# sales_report.py
from typing import Iterable

Order = dict[str, object]

ORDERS: list[Order] = [
    {"id": 1, "region": "North", "amount": 1200.50, "status": "paid"},
    {"id": 2, "region": "South", "amount": 890.00, "status": "paid"},
    {"id": 3, "region": "North", "amount": 450.25, "status": "refunded"},
    {"id": 4, "region": "East",  "amount": 2100.75, "status": "paid"},
    {"id": 5, "region": "South", "amount": 310.00, "status": "pending"},
]

def filter_paid(orders: Iterable[Order]) -> list[Order]:
    """Return only the orders with status 'paid'."""
    return [o for o in orders if o["status"] == "paid"]

def total_by_region(orders: Iterable[Order]) -> dict[str, float]:
    """Sum order amounts grouped by region."""
    totals: dict[str, float] = {}
    for o in orders:
        region = str(o["region"])
        totals[region] = totals.get(region, 0.0) + float(o["amount"])
    return totals

def format_report(totals: dict[str, float]) -> str:
    """Render the per-region totals and the grand total."""
    lines = [f"{r}: ${totals[r]:,.2f}" for r in sorted(totals)]
    lines.append(f"TOTAL: ${sum(totals.values()):,.2f}")
    return "\n".join(lines)

def main() -> None:
    print(format_report(total_by_region(filter_paid(ORDERS))))

if __name__ == "__main__":
    main()

