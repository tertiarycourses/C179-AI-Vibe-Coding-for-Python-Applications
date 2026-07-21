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

