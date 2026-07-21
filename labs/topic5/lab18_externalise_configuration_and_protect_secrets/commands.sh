#!/usr/bin/env bash
# Lab 18 — Externalise Configuration and Protect Secrets
set -euo pipefail

# 1. Find every hard-coded value in the project
grep -rn '127.0.0.1\|8000\|cardguard.db\|0.55\|0.80' --include='*.py' . | grep -v '.venv'

# 2. Add typed settings
uv add pydantic-settings

# 8. Prove configuration is live — override without editing any code
uv run python -c "
from config import settings
print('default review threshold:', settings.review_threshold)
"
CARDGUARD_REVIEW_THRESHOLD=0.30 uv run python -c "
from config import settings
print('overridden by environment:', settings.review_threshold)
"

# 9. Confirm .env is genuinely ignored
git check-ignore -v .env && echo 'SAFE: .env will not be committed'
