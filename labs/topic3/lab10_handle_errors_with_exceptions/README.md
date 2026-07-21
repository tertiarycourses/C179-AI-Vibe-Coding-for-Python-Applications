# Lab 10 — Handle Errors with Exceptions

**Topic 3** · Use try/except/else/finally and raise meaningful custom exceptions

The learner makes the loader robust: catching the specific failures that actually occur, defining a custom exception hierarchy for the domain, and guaranteeing cleanup with finally. A screening service that crashes on one bad row fails open — this lab prevents that.

- **You will build:** A domain exception hierarchy plus a validated, fail-safe loader
- **Tools:** uv, pandas, sqlite3, Python exceptions

## Steps

1. Define exceptions that describe the DOMAIN, not the plumbing

   ```python
   # errors.py
   class CardGuardError(Exception):
       """Base class for every CardGuard failure — callers can catch this one type."""
   
   class DataSourceError(CardGuardError):
       """The transaction store could not be read."""
   
   class ValidationError(CardGuardError):
       """A transaction failed validation before scoring."""
       def __init__(self, field: str, value, message: str):
           self.field, self.value = field, value
           super().__init__(f"{field}={value!r}: {message}")
   
   class RuleExecutionError(CardGuardError):
       """A scoring rule raised while screening a transaction."""
   ```

2. Catch the SPECIFIC errors that happen, and translate them to domain errors

   ```python
   # analytics.py (updated)
   import sqlite3
   from pathlib import Path
   import pandas as pd
   from errors import DataSourceError
   
   def load_transactions(db_path: str = "cardguard.db") -> pd.DataFrame:
       """Load transactions, raising DataSourceError on any read failure."""
       if not Path(db_path).exists():
           raise DataSourceError(f"database not found: {db_path}")
       con = None
       try:
           con = sqlite3.connect(db_path)
           df = pd.read_sql_query("SELECT * FROM transactions", con)
       except sqlite3.DatabaseError as exc:
           raise DataSourceError(f"could not read {db_path}: {exc}") from exc
       else:
           df["ts"] = pd.to_datetime(df["ts"])
           df["hour"] = df["ts"].dt.hour
           return df
       finally:
           if con is not None:
               con.close()      # runs on success AND on failure
   ```

3. Prove each failure path raises the right domain error

   ```bash
   uv run python -c "
   from analytics import load_transactions
   from errors import DataSourceError
   try:
       load_transactions('no_such.db')
   except DataSourceError as e:
       print('missing file ->', e)
   open('corrupt.db','wb').write(b'not a database at all')
   try:
       load_transactions('corrupt.db')
   except DataSourceError as e:
       print('corrupt file ->', type(e).__name__)
   "
   ```

4. Validate a transaction and raise ValidationError carrying the offending field

   ```python
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
   ```

5. Run a batch where some records are bad — the batch must NOT die on the first failure

   ```bash
   uv run python -c "
   from validate import validate_txn
   from errors import ValidationError
   batch = [
     {'amount': 120.0, 'merchant_category': 'grocery'},
     {'amount': -5.0,  'merchant_category': 'fuel'},
     {'amount': 'abc', 'merchant_category': 'grocery'},
     {'amount': 90.0,  'merchant_category': 'casino'},
     {'amount': 45.0,  'merchant_category': 'transport'},
   ]
   ok, rejected = [], []
   for i, rec in enumerate(batch):
       try:
           ok.append(validate_txn(rec))
       except ValidationError as e:
           rejected.append((i, str(e)))
   print(f'accepted {len(ok)}, rejected {len(rejected)}')
   for i, msg in rejected:
       print(f'  row {i}: {msg}')
   "
   ```

6. Contrast with the anti-pattern — a bare except hides the bug you needed to see

   ```bash
   uv run python -c "
   # ANTI-PATTERN: never do this
   try:
       result = 1 / 0
   except:              # catches everything, including typos and KeyboardInterrupt
       result = 0
   print('silently wrong:', result)
   
   # Correct: name the exception you expect and can handle
   try:
       result = 1 / 0
   except ZeroDivisionError as e:
       print('handled explicitly:', e)
   "
   ```

7. Ask your assistant to add a rule-level guard so one broken rule cannot stop a screen

   ```python
   Ask the assistant: In RuleEngine.screen, wrap each rule call in try/except so that if one rule raises, the engine records a RuleExecutionError message on the result and continues scoring with the remaining rules. Never use a bare except.
   ```


## Verify

Missing and corrupt databases raise DataSourceError; the 5-record batch accepts 2 and rejects 3 with field-level messages; the learner can explain why bare except is unsafe.
