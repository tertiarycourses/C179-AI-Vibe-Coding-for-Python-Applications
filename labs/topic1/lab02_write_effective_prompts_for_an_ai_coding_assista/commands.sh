#!/usr/bin/env bash
# Lab 2 — Write Effective Prompts for an AI Coding Assistant
set -euo pipefail

# 5. Test the boundaries the prompt specified — this is where generated code usually fails
uv run python -c "
from scoring import score_transaction
print(score_transaction(42.90, False, 14))   # low risk
print(score_transaction(800.00, True, 3))    # every rule fires
print(score_transaction(500.00, False, 14))  # exactly on the threshold
"

# 6. Confirm the error paths actually raise
uv run python -c "
from scoring import score_transaction
try:
    score_transaction(-100, False, 14)
except ValueError as e:
    print('correctly raised:', e)
"
