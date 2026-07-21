#!/usr/bin/env bash
# Lab 20 — Deploy the Full Stack with Docker Compose
set -euo pipefail

# 4. Bring the stack up
docker compose up --build -d

# 5. Confirm the UI waited for the API to become healthy
docker compose ps
docker compose logs api --tail 5

# 6. Seed the database inside the running container
docker compose exec api python mockdata.py
docker compose exec api ls -la /data

# 7. Verify end to end through the browser — screen a fraudulent charge in the UI
open http://localhost:8501

# 8. Verify the API tier independently
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/stats | python3 -m json.tool

# 9. Confirm data survives a restart — this is what the volume is for
docker compose restart api
sleep 5
curl -s http://127.0.0.1:8000/stats | python3 -m json.tool

# 10. Tear down, keeping the data volume
docker compose down
docker volume ls | grep cardguard
