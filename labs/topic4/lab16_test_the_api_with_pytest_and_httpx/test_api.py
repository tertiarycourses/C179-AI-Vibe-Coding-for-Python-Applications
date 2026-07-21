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

