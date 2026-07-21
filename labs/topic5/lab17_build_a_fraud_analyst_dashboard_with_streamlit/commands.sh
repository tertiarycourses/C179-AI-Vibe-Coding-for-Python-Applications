#!/usr/bin/env bash
# Lab 17 — Build a Fraud Analyst Dashboard with Streamlit
set -euo pipefail

# 1. Add Streamlit
uv add streamlit httpx

# 5. Screen a normal transaction in the UI and watch it land in the queue
open http://localhost:8501
