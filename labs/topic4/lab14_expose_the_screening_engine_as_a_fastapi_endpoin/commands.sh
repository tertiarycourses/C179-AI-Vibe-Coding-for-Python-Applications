#!/usr/bin/env bash
# Lab 14 — Expose the Screening Engine as a FastAPI Endpoint
set -euo pipefail

# 1. Add the web dependencies
uv add fastapi uvicorn[standard] httpx

# 3. Start the server
uv run uvicorn main:app --reload --port 8000

# 4. Open the auto-generated interactive docs — you wrote no OpenAPI spec
open http://127.0.0.1:8000/docs

# 5. Screen a clearly fraudulent transaction
curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH0023","ts":"2026-04-15T02:14:00","amount":5128.33,"merchant_category":"jewellery","city":"Singapore","lat":1.3521,"lon":103.8198}' | python3 -m json.tool

# 6. Screen a normal grocery run and compare the decision
curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH0001","ts":"2026-04-15T10:30:00","amount":86.40,"merchant_category":"grocery","city":"Singapore","lat":1.3521,"lon":103.8198}' | python3 -m json.tool

# 7. Send invalid input — FastAPI rejects it with 422 before your code runs
curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"NOPE","ts":"2026-04-15T10:30:00","amount":-5,"merchant_category":"casino","city":"S","lat":1.35,"lon":103.8}' | python3 -m json.tool

# 8. Send an unknown card and confirm the 404 path
curl -s -i -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH9999","ts":"2026-04-15T10:30:00","amount":50,"merchant_category":"grocery","city":"Singapore","lat":1.35,"lon":103.8}' | head -1
