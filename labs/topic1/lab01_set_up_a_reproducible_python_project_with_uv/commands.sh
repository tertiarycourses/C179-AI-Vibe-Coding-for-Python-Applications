#!/usr/bin/env bash
# Lab 1 — Set Up a Reproducible Python Project with uv
set -euo pipefail

# 1. Confirm uv is installed and check the version
uv --version

# 2. Create a new project folder and initialise it
uv init cardguard
cd cardguard

# 3. Inspect what uv generated — note pyproject.toml is the project manifest
ls -a
cat pyproject.toml

# 4. Pin the Python version so every learner runs the same interpreter
uv python pin 3.12

# 5. Add a dependency — uv resolves, installs and writes uv.lock in one step
uv add pandas

# 8. Run it through uv — no venv activation needed
uv run python main.py

# 9. Prove reproducibility: delete the venv and restore it from the lockfile
rm -rf .venv
uv sync
uv run python main.py
