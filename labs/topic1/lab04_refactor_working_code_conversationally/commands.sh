#!/usr/bin/env bash
# Lab 4 — Refactor Working Code Conversationally
set -euo pipefail

# 2. Capture the baseline output to a file — this is the contract the refactor must preserve
uv run python sales_report.py > baseline.txt
cat baseline.txt

# 5. Prove the behaviour is unchanged by diffing against the baseline
uv run python sales_report.py > after.txt
diff baseline.txt after.txt && echo 'IDENTICAL — refactor is safe'

# 6. Now that the logic is in functions, test one piece in isolation — impossible before the refactor
uv run python -c "
from sales_report import total_by_region
rows = [{'region': 'North', 'amount': 100.0, 'status': 'paid'},
        {'region': 'North', 'amount': 50.0,  'status': 'paid'}]
assert total_by_region(rows) == {'North': 150.0}
print('unit test passed')
"
