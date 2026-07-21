# Lab 4 — Refactor Working Code Conversationally

**Topic 1** · Use an AI assistant to restructure code without changing its behaviour

The learner takes a working but poorly structured script, establishes a behavioural baseline, refactors it into small testable functions with AI assistance, and proves the output is unchanged.

- **You will build:** A refactored sales summary script with an unchanged, verified output
- **Tools:** AI coding assistant, uv, Python

## Steps

1. Save the working script — it produces correct output but is one long block

   ```python
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
   ```

2. Capture the baseline output to a file — this is the contract the refactor must preserve

   ```bash
   uv run python sales_report.py > baseline.txt
   cat baseline.txt
   ```

3. Ask for a structural refactor and state explicitly that behaviour must not change

   ```python
   Ask the assistant: Refactor sales_report.py into three functions — filter_paid(orders), total_by_region(orders) and format_report(totals) — plus a main() guarded by if __name__ == '__main__'. Add type hints. The printed output must be byte-for-byte identical to the current version.
   ```

4. Save the refactored version

   ```python
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
   ```

5. Prove the behaviour is unchanged by diffing against the baseline

   ```bash
   uv run python sales_report.py > after.txt
   diff baseline.txt after.txt && echo 'IDENTICAL — refactor is safe'
   ```

6. Now that the logic is in functions, test one piece in isolation — impossible before the refactor

   ```bash
   uv run python -c "
   from sales_report import total_by_region
   rows = [{'region': 'North', 'amount': 100.0, 'status': 'paid'},
           {'region': 'North', 'amount': 50.0,  'status': 'paid'}]
   assert total_by_region(rows) == {'North': 150.0}
   print('unit test passed')
   "
   ```

7. Note the sequence that makes refactoring safe: baseline first, refactor second, diff third.

## Verify

diff reports no difference between baseline.txt and after.txt, and total_by_region can be unit-tested independently.
