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

