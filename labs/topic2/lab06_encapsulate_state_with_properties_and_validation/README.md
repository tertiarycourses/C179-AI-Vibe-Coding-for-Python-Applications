# Lab 6 — Encapsulate State with Properties and Validation

**Topic 2** · Protect object state behind a controlled interface

The learner builds a Cardholder class whose running spend baseline cannot be corrupted from outside, using private attributes, a read-only property and validation in the setter.

- **You will build:** A Cardholder class with a protected baseline and a validated update method
- **Tools:** uv, Python 3.12

## Steps

1. Write the class with state deliberately kept private

   ```python
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
   ```

2. Add the only sanctioned way to move the baseline

   ```python
       def observe(self, amount: float) -> None:
           """Fold one new transaction into the running baseline."""
           if amount < 0:
               raise ValueError("amount must not be negative")
           self._observed_count += 1
           weight = 1 / min(self._observed_count, 30)   # rolling, recency-weighted
           self._typical_amount = (1 - weight) * self._typical_amount + weight * amount
   
       def deviation_factor(self, amount: float) -> float:
           """How many times the baseline this amount represents."""
           return round(amount / self._typical_amount, 2)
   ```

3. Prove the baseline cannot be overwritten from outside

   ```bash
   uv run python -c "
   from cardholder import Cardholder
   ch = Cardholder('CH0001', 'Aisha Tan', 'Singapore', 120.0)
   try:
       ch.typical_amount = 999999
   except AttributeError as e:
       print('blocked:', e)
   "
   ```

4. Drive the baseline the sanctioned way and watch it move

   ```bash
   uv run python -c "
   from cardholder import Cardholder
   ch = Cardholder('CH0001', 'Aisha Tan', 'Singapore', 120.0)
   for amt in [110, 130, 125, 118, 122]:
       ch.observe(amt)
   print('baseline', ch.typical_amount, 'after', ch.observed_count, 'observations')
   print('a $2,400 charge is', ch.deviation_factor(2400), 'x baseline')
   "
   ```

5. Confirm validation rejects bad input at both entry points

   ```bash
   uv run python -c "
   from cardholder import Cardholder
   for bad in [lambda: Cardholder('C','n','SG',0), lambda: Cardholder('C','n','SG',120).observe(-5)]:
       try:
           bad(); print('NOT CAUGHT')
       except ValueError as e:
           print('correctly raised:', e)
   "
   ```

6. Load the real cardholders and rank them by baseline

   ```bash
   uv run python -c "
   import sqlite3
   from cardholder import Cardholder
   con = sqlite3.connect('cardguard.db')
   rows = con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders').fetchall()
   chs = [Cardholder(*r) for r in rows]
   top = sorted(chs, key=lambda c: c.typical_amount, reverse=True)[:5]
   for c in top:
       print(f'{c.card_ref} {c.name:<16} baseline ${c.typical_amount:,.2f}')
   "
   ```

7. Note why this matters for fraud: if any caller could assign typical_amount directly, an attacker-controlled input path could raise the baseline until nothing looks anomalous.

## Verify

Assigning to typical_amount raises AttributeError; observe() updates the baseline; both constructors and observe() reject invalid values; the 5 highest baselines print from the database.
