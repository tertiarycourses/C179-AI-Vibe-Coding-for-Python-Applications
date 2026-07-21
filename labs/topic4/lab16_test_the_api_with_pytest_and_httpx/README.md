# Lab 16 — Test the API with pytest and httpx

**Topic 4** · Write automated tests for a FastAPI application

The learner writes a test suite covering the happy path, validation failures and persistence — so that later refactoring and deployment changes are provably safe.

- **You will build:** A passing pytest suite against the screening API
- **Tools:** uv, pytest, FastAPI TestClient

## Steps

1. Add the test dependencies

   ```bash
   uv add --dev pytest httpx
   ```

2. Write tests for the decision paths

   ```python
   # test_api.py
   import pytest
   from fastapi.testclient import TestClient
   from main import app
   
   client = TestClient(app)
   
   def post(**overrides):
       body = {"card_ref": "CH0001", "ts": "2026-04-15T10:30:00", "amount": 86.40,
               "merchant_category": "grocery", "city": "Singapore",
               "lat": 1.3521, "lon": 103.8198}
       body.update(overrides)
       return client.post("/screen", json=body)
   
   def test_health():
       assert client.get("/health").json() == {"status": "ok"}
   
   def test_normal_transaction_is_approved():
       r = post()
       assert r.status_code == 200
       assert r.json()["decision"] == "approve"
   
   def test_large_offhours_transaction_is_escalated():
       r = post(amount=5128.33, merchant_category="jewellery", ts="2026-04-15T02:14:00")
       body = r.json()
       assert body["decision"] in {"review", "decline"}
       assert body["hits"], "an escalated decision must carry its reasons"
   ```

3. Add tests for the failure paths

   ```python
   # test_api.py (add)
   @pytest.mark.parametrize("bad", [
       {"amount": -5},
       {"amount": 0},
       {"card_ref": "NOPE"},
       {"merchant_category": "casino"},
       {"lat": 999},
   ])
   def test_invalid_input_is_rejected(bad):
       assert post(**bad).status_code == 422
   
   def test_unknown_card_returns_404():
       assert post(card_ref="CH9999").status_code == 404
   
   def test_screening_is_persisted():
       before = len(client.get("/screenings?limit=1000").json())
       post()
       after = len(client.get("/screenings?limit=1000").json())
       assert after == before + 1
   ```

4. Run the suite

   ```bash
   uv run pytest -v
   ```

5. Check what the tests actually cover

   ```bash
   uv add --dev pytest-cov
   uv run pytest --cov=. --cov-report=term-missing
   ```

6. Ask your assistant to write a test for a gap — then verify it FAILS first

   ```python
   Ask the assistant: Write a pytest test asserting that POST /screen with amount exactly 1000000 succeeds but 1000001 returns 422, matching the Field(le=1_000_000) constraint in TransactionIn.
   ```

7. Note the discipline: a test you have never seen fail is a test you cannot trust.

## Verify

All tests pass; invalid inputs are parameterised and rejected with 422; the persistence test proves a row is written per screening.
