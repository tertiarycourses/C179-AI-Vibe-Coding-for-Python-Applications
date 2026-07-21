# Lab 14 — Expose the Screening Engine as a FastAPI Endpoint

**Topic 4** · Turn typed Python functions into HTTP endpoints

The learner wraps the Topic 2 RuleEngine in a FastAPI POST endpoint. The engine is not modified at all — FastAPI is a thin transport layer over logic that already works.

- **You will build:** A running API with POST /screen, GET /health and automatic OpenAPI docs
- **Tools:** uv, FastAPI, uvicorn, Pydantic

## Steps

1. Add the web dependencies

   ```bash
   uv add fastapi uvicorn[standard] httpx
   ```

2. Write the application — note how little code the endpoint needs

   ```python
   # main.py
   import sqlite3
   from fastapi import FastAPI, HTTPException
   from schemas import TransactionIn, ScreeningOut, RuleHit
   from models import Transaction
   from cardholder import Cardholder
   from rules import AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule, VelocityRule
   from engine import RuleEngine
   
   app = FastAPI(title="CardGuard Screening API", version="1.0.0")
   
   ENGINE = RuleEngine([AmountDeviationRule(), UnusualHourRule(),
                        HighRiskCategoryRule(), VelocityRule()])
   
   def get_holder(card_ref: str) -> Cardholder:
       con = sqlite3.connect("cardguard.db")
       try:
           row = con.execute("SELECT card_ref,name,home_city,typical_amount "
                             "FROM cardholders WHERE card_ref=?", (card_ref,)).fetchone()
       finally:
           con.close()
       if row is None:
           raise HTTPException(status_code=404, detail=f"unknown card_ref {card_ref}")
       return Cardholder(*row)
   
   def decide(score: float) -> str:
       if score >= 0.80: return "decline"
       if score >= 0.55: return "review"
       return "approve"
   
   @app.get("/health")
   def health() -> dict:
       return {"status": "ok"}
   
   @app.post("/screen", response_model=ScreeningOut)
   def screen(txn_in: TransactionIn) -> ScreeningOut:
       """Score one transaction and return the decision with reasons."""
       holder = get_holder(txn_in.card_ref)
       txn = Transaction(id=0, card_ref=txn_in.card_ref, ts=txn_in.ts,
                         amount=txn_in.amount, merchant_category=txn_in.merchant_category,
                         city=txn_in.city, lat=txn_in.lat, lon=txn_in.lon)
       result = ENGINE.screen(txn, holder, [])
       return ScreeningOut(card_ref=result.card_ref,
                           composite_score=result.composite_score,
                           flagged=result.flagged,
                           decision=decide(result.composite_score),
                           hits=[RuleHit(rule_name=r.rule_name, score=r.score, reason=r.reason)
                                 for r in result.results if r.score > 0],
                           errors=result.errors)
   ```

3. Start the server

   ```bash
   uv run uvicorn main:app --reload --port 8000
   ```

4. Open the auto-generated interactive docs — you wrote no OpenAPI spec

   ```bash
   open http://127.0.0.1:8000/docs
   ```

5. Screen a clearly fraudulent transaction

   ```bash
   curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH0023","ts":"2026-04-15T02:14:00","amount":5128.33,"merchant_category":"jewellery","city":"Singapore","lat":1.3521,"lon":103.8198}' | python3 -m json.tool
   ```

6. Screen a normal grocery run and compare the decision

   ```bash
   curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH0001","ts":"2026-04-15T10:30:00","amount":86.40,"merchant_category":"grocery","city":"Singapore","lat":1.3521,"lon":103.8198}' | python3 -m json.tool
   ```

7. Send invalid input — FastAPI rejects it with 422 before your code runs

   ```bash
   curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"NOPE","ts":"2026-04-15T10:30:00","amount":-5,"merchant_category":"casino","city":"S","lat":1.35,"lon":103.8}' | python3 -m json.tool
   ```

8. Send an unknown card and confirm the 404 path

   ```bash
   curl -s -i -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" -d '{"card_ref":"CH9999","ts":"2026-04-15T10:30:00","amount":50,"merchant_category":"grocery","city":"Singapore","lat":1.35,"lon":103.8}' | head -1
   ```


## Verify

GET /health returns ok; the fraud transaction returns decline with reasons; the grocery transaction returns approve; bad input returns 422; an unknown card returns 404.
