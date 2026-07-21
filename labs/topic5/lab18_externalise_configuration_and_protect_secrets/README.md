# Lab 18 — Externalise Configuration and Protect Secrets

**Topic 5** · Move settings out of code into the environment

The learner replaces every hard-coded value with typed settings loaded from the environment, and ensures secrets can never be committed — the change that makes the same image runnable in dev and production.

- **You will build:** A typed Settings object, a .env file and a .gitignore that excludes it
- **Tools:** uv, pydantic-settings, python-dotenv

## Steps

1. Find every hard-coded value in the project

   ```bash
   grep -rn '127.0.0.1\|8000\|cardguard.db\|0.55\|0.80' --include='*.py' . | grep -v '.venv'
   ```

2. Add typed settings

   ```bash
   uv add pydantic-settings
   ```

3. Declare configuration as a validated model

   ```python
   # config.py
   from pydantic_settings import BaseSettings, SettingsConfigDict
   
   class Settings(BaseSettings):
       """All runtime configuration, validated at startup."""
       model_config = SettingsConfigDict(env_file=".env", env_prefix="CARDGUARD_")
   
       db_path: str = "cardguard.db"
       api_url: str = "http://127.0.0.1:8000"
       review_threshold: float = 0.55
       decline_threshold: float = 0.80
       velocity_window_minutes: int = 10
       log_level: str = "INFO"
   
   settings = Settings()
   ```

4. Create .env for local development and EXCLUDE it from git immediately

   ```python
   # .env
   CARDGUARD_DB_PATH=cardguard.db
   CARDGUARD_REVIEW_THRESHOLD=0.55
   CARDGUARD_DECLINE_THRESHOLD=0.80
   CARDGUARD_LOG_LEVEL=DEBUG
   ```

5. Add the gitignore entries BEFORE the first commit

   ```python
   # .gitignore
   .env
   .env.*
   !.env.example
   .venv/
   __pycache__/
   *.db
   .pytest_cache/
   ```

6. Commit a .env.example instead, so a new joiner knows what to set

   ```python
   # .env.example — safe to commit, contains no real values
   CARDGUARD_DB_PATH=cardguard.db
   CARDGUARD_REVIEW_THRESHOLD=0.55
   CARDGUARD_DECLINE_THRESHOLD=0.80
   CARDGUARD_LOG_LEVEL=INFO
   ```

7. Replace the hard-coded thresholds with settings

   ```python
   # main.py (replace decide())
   from config import settings
   
   def decide(score: float) -> str:
       if score >= settings.decline_threshold: return "decline"
       if score >= settings.review_threshold:  return "review"
       return "approve"
   ```

8. Prove configuration is live — override without editing any code

   ```bash
   uv run python -c "
   from config import settings
   print('default review threshold:', settings.review_threshold)
   "
   CARDGUARD_REVIEW_THRESHOLD=0.30 uv run python -c "
   from config import settings
   print('overridden by environment:', settings.review_threshold)
   "
   ```

9. Confirm .env is genuinely ignored

   ```bash
   git check-ignore -v .env && echo 'SAFE: .env will not be committed'
   ```


## Verify

Settings load from .env; an environment variable overrides them without a code change; git check-ignore confirms .env is excluded; .env.example is committed in its place.
