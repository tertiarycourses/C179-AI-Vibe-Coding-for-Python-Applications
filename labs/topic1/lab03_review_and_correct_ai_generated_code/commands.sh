#!/usr/bin/env bash
# Lab 3 — Review and Correct AI-Generated Code
set -euo pipefail

# 2. Probe it with the values a real order system would send
uv run python -c "
from discount import apply_discount
print(apply_discount(100, 'gold'))
print(apply_discount(100, 'GOLD'))
print(apply_discount(100, None))
print(apply_discount(-50, 'gold'))
print(apply_discount(100.555, 'silver'))
"

# 6. Re-run every probe that previously failed
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
