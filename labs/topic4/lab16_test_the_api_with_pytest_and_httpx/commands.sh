#!/usr/bin/env bash
# Lab 16 — Test the API with pytest and httpx
set -euo pipefail

# 1. Add the test dependencies
uv add --dev pytest httpx

# 4. Run the suite
uv run pytest -v

# 5. Check what the tests actually cover
uv add --dev pytest-cov
uv run pytest --cov=. --cov-report=term-missing
