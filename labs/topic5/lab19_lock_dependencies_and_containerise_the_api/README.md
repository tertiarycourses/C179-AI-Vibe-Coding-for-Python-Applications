# Lab 19 — Lock Dependencies and Containerise the API

**Topic 5** · Package the application into a reproducible image

The learner writes a multi-stage Dockerfile that installs from uv.lock, runs as a non-root user, and produces an image that behaves identically on any machine.

- **You will build:** A built Docker image running the screening API with a health check
- **Tools:** uv, Docker, uvicorn

## Steps

1. Confirm the lockfile is current and committed

   ```bash
   uv lock --check
   git add uv.lock pyproject.toml
   ```

2. Write the Dockerfile — multi-stage keeps the final image small

   ```python
   # Dockerfile
   FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
   WORKDIR /app
   ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
   
   # Install dependencies first so this layer caches across code changes
   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-install-project --no-dev
   
   COPY . .
   RUN uv sync --frozen --no-dev
   
   FROM python:3.12-slim-bookworm AS runtime
   RUN useradd --create-home --uid 1000 appuser
   WORKDIR /app
   COPY --from=builder --chown=appuser:appuser /app /app
   ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
   USER appuser
   EXPOSE 8000
   HEALTHCHECK --interval=30s --timeout=3s --retries=3 \\
     CMD python -c "import httpx,sys; sys.exit(0 if httpx.get('http://127.0.0.1:8000/health').status_code==200 else 1)"
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. Exclude everything the image does not need

   ```python
   # .dockerignore
   .venv/
   .git/
   .env
   *.db
   __pycache__/
   .pytest_cache/
   tests/
   *.md
   ```

4. Build the image

   ```bash
   docker build -t cardguard-api:1.0 .
   ```

5. Check the size — multi-stage should keep it well under 300MB

   ```bash
   docker images cardguard-api:1.0
   ```

6. Run it, passing configuration as environment variables

   ```bash
   docker run -d --name cardguard \
     -p 8000:8000 \
     -e CARDGUARD_REVIEW_THRESHOLD=0.55 \
     -e CARDGUARD_LOG_LEVEL=INFO \
     -v "$(pwd)/cardguard.db:/app/cardguard.db" \
     cardguard-api:1.0
   ```

7. Verify the container is healthy and answering

   ```bash
   docker ps --filter name=cardguard --format 'table {{.Names}}\t{{.Status}}'
   curl -s http://127.0.0.1:8000/health
   ```

8. Screen a transaction against the CONTAINER, not your laptop's Python

   ```bash
   curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH0023","ts":"2026-04-15T02:14:00","amount":5128.33,"merchant_category":"jewellery","city":"Singapore","lat":1.3521,"lon":103.8198}' | python3 -m json.tool
   ```

9. Read the logs and confirm it runs as a non-root user

   ```bash
   docker logs cardguard --tail 20
   docker exec cardguard whoami
   ```


## Verify

The image builds, runs as appuser, reports healthy, and returns a decline decision for the fraud transaction posted to the container.
