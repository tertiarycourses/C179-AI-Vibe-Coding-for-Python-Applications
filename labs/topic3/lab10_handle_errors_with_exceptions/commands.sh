#!/usr/bin/env bash
# Lab 10 — Handle Errors with Exceptions
set -euo pipefail

# 3. Prove each failure path raises the right domain error
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

# 5. Run a batch where some records are bad — the batch must NOT die on the first failure
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

# 6. Contrast with the anti-pattern — a bare except hides the bug you needed to see
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
