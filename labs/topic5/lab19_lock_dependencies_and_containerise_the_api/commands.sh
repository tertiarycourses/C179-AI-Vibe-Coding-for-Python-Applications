#!/usr/bin/env bash
# Lab 19 — Lock Dependencies and Containerise the API
set -euo pipefail

# 1. Confirm the lockfile is current and committed
uv lock --check
git add uv.lock pyproject.toml

# 4. Build the image
docker build -t cardguard-api:1.0 .

# 5. Check the size — multi-stage should keep it well under 300MB
docker images cardguard-api:1.0

# 6. Run it, passing configuration as environment variables
docker run -d --name cardguard \
  -p 8000:8000 \
  -e CARDGUARD_REVIEW_THRESHOLD=0.55 \
  -e CARDGUARD_LOG_LEVEL=INFO \
  -v "$(pwd)/cardguard.db:/app/cardguard.db" \
  cardguard-api:1.0

# 7. Verify the container is healthy and answering
docker ps --filter name=cardguard --format 'table {{.Names}}\t{{.Status}}'
curl -s http://127.0.0.1:8000/health

# 8. Screen a transaction against the CONTAINER, not your laptop's Python
curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH0023","ts":"2026-04-15T02:14:00","amount":5128.33,"merchant_category":"jewellery","city":"Singapore","lat":1.3521,"lon":103.8198}' | python3 -m json.tool

# 9. Read the logs and confirm it runs as a non-root user
docker logs cardguard --tail 20
docker exec cardguard whoami
