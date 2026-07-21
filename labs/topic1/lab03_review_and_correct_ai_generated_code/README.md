# Lab 3 — Review and Correct AI-Generated Code

**Topic 1** · Identify and fix defects in code produced by an AI assistant

The learner is given a plausible but subtly wrong implementation, finds the defects by testing rather than by reading alone, and corrects them. This lab establishes that the developer, not the assistant, owns correctness.

- **You will build:** A corrected discount calculator plus a short defect log
- **Tools:** AI coding assistant, uv, Python

## Steps

1. Save this generated function exactly as written — it looks reasonable

   ```python
   # discount.py
   def apply_discount(price, tier):
       if tier == "gold":
           return price * 0.8
       elif tier == "silver":
           return price * 0.9
       elif tier == "bronze":
           return price * 0.95
       return price
   ```

2. Probe it with the values a real order system would send

   ```bash
   uv run python -c "
   from discount import apply_discount
   print(apply_discount(100, 'gold'))
   print(apply_discount(100, 'GOLD'))
   print(apply_discount(100, None))
   print(apply_discount(-50, 'gold'))
   print(apply_discount(100.555, 'silver'))
   "
   ```

3. Record the defects you found: case sensitivity, no validation of price, unrounded currency, silent fallthrough on an unknown tier, and no type hints.
4. Ask the assistant to fix the specific defects — name them, do not say 'improve this'

   ```python
   Ask the assistant: Fix these defects in apply_discount: (1) tier matching must be case-insensitive, (2) raise ValueError for a negative price, (3) raise ValueError for an unrecognised tier instead of silently returning the full price, (4) round the result to 2 decimal places, (5) add type hints and a docstring.
   ```

5. Review the corrected version line by line before accepting it

   ```python
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
   ```

6. Re-run every probe that previously failed

   ```bash
   uv run python -c "
   from discount import apply_discount
   print(apply_discount(100, 'GOLD'))
   print(apply_discount(100.555, 'silver'))
   for bad in [(-50, 'gold'), (100, 'platinum'), (100, None)]:
       try:
           apply_discount(*bad)
           print('NOT CAUGHT:', bad)
       except ValueError as e:
           print('correctly raised:', e)
   "
   ```

7. Note the lesson: the first version ran without error on the happy path. Running is not the same as correct.

## Verify

All five defects are fixed and demonstrated by tests. The learner can explain why reading alone did not reveal them.
