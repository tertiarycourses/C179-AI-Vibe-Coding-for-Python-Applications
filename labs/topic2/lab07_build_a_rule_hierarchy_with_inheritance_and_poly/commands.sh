#!/usr/bin/env bash
# Lab 7 — Build a Rule Hierarchy with Inheritance and Polymorphism
set -euo pipefail

# 2. Prove the abstract class cannot be instantiated — the contract is enforced
uv run python -c "
from rules import FraudRule
try:
    FraudRule()
except TypeError as e:
    print('correctly blocked:', e)
"

# 6. Call every rule through the SAME interface — this is polymorphism doing real work
uv run python -c "
import sqlite3
from models import Transaction
from cardholder import Cardholder
from rules import AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule, VelocityRule
con = sqlite3.connect('cardguard.db')
row = con.execute('SELECT * FROM transactions WHERE is_known_fraud=1 ORDER BY amount DESC LIMIT 1').fetchone()
txn = Transaction.from_row(row)
chr_ = con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders WHERE card_ref=?', (txn.card_ref,)).fetchone()
holder = Cardholder(*chr_)
rules = [AmountDeviationRule(), UnusualHourRule(), HighRiskCategoryRule(), VelocityRule()]
print(txn)
for r in rules:
    res = r.score(txn, holder, [])
    print(f'  {res.rule_name:<24} {res.score:>5}  {res.reason}')
"
