# Lab 20 — Deploy the Full Stack with Docker Compose

**Topic 5** · Run and verify a multi-service application

The learner composes the API and the Streamlit UI into one stack with a shared volume and dependency ordering, then verifies the deployment end to end — the final integration of everything built in Topics 1-5.

- **You will build:** A running two-service stack verified with a real screening through the UI
- **Tools:** Docker Compose, FastAPI, Streamlit, SQLite

## Steps

1. Write a Dockerfile for the UI tier

   ```python
   # Dockerfile.ui
   FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
   WORKDIR /app
   ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-dev
   COPY . .
   ENV PATH="/app/.venv/bin:$PATH"
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
   ```

2. Compose the stack

   ```python
   # compose.yaml
   services:
     api:
       build: .
       ports: ["8000:8000"]
       environment:
         CARDGUARD_DB_PATH: /data/cardguard.db
         CARDGUARD_REVIEW_THRESHOLD: "0.55"
         CARDGUARD_DECLINE_THRESHOLD: "0.80"
       volumes: ["cardguard-data:/data"]
       healthcheck:
         test: ["CMD", "python", "-c", "import httpx,sys; sys.exit(0 if httpx.get('http://127.0.0.1:8000/health').status_code==200 else 1)"]
         interval: 10s
         timeout: 3s
         retries: 5
   
     ui:
       build:
         context: .
         dockerfile: Dockerfile.ui
       ports: ["8501:8501"]
       environment:
         CARDGUARD_API_URL: http://api:8000
       depends_on:
         api:
           condition: service_healthy
   
   volumes:
     cardguard-data:
   ```

3. Point the UI at the service name — inside the network it is not localhost

   ```python
   # app.py (replace the API constant)
   import os
   API = os.getenv("CARDGUARD_API_URL", "http://127.0.0.1:8000")
   ```

4. Bring the stack up

   ```bash
   docker compose up --build -d
   ```

5. Confirm the UI waited for the API to become healthy

   ```bash
   docker compose ps
   docker compose logs api --tail 5
   ```

6. Seed the database inside the running container

   ```bash
   docker compose exec api python mockdata.py
   docker compose exec api ls -la /data
   ```

7. Verify end to end through the browser — screen a fraudulent charge in the UI

   ```bash
   open http://localhost:8501
   ```

8. Verify the API tier independently

   ```bash
   curl -s http://127.0.0.1:8000/health
   curl -s http://127.0.0.1:8000/stats | python3 -m json.tool
   ```

9. Confirm data survives a restart — this is what the volume is for

   ```bash
   docker compose restart api
   sleep 5
   curl -s http://127.0.0.1:8000/stats | python3 -m json.tool
   ```

10. Tear down, keeping the data volume

   ```bash
   docker compose down
   docker volume ls | grep cardguard
   ```


## Verify

Both services start, the UI waits for the API health check, a screening submitted in the browser is stored and visible via /stats, and the data survives a container restart.
