#!/usr/bin/env bash
# Lab 8 — Compose Rules into an Engine
set -euo pipefail

# 3. Screen a known-fraud transaction and read the explanation
uv run python -c "
import sqlite3
from models import Transaction
from cardholder import Cardholder
from rules import AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule, VelocityRule
from engine import RuleEngine
con = sqlite3.connect('cardguard.db')
row = con.execute('SELECT * FROM transactions WHERE is_known_fraud=1 ORDER BY amount DESC LIMIT 1').fetchone()
txn = Transaction.from_row(row)
holder = Cardholder(*con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders WHERE card_ref=?',(txn.card_ref,)).fetchone())
eng = RuleEngine([AmountDeviationRule(), UnusualHourRule(), HighRiskCategoryRule(), VelocityRule()])
print(eng.screen(txn, holder, []).explain())
"

# 4. Screen a normal transaction and confirm it stays clean
uv run python -c "
import sqlite3
from models import Transaction
from cardholder import Cardholder
from rules import AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule, VelocityRule
from engine import RuleEngine
con = sqlite3.connect('cardguard.db')
row = con.execute("SELECT * FROM transactions WHERE is_known_fraud=0 AND merchant_category='grocery' LIMIT 1").fetchone()
txn = Transaction.from_row(row)
holder = Cardholder(*con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders WHERE card_ref=?',(txn.card_ref,)).fetchone())
eng = RuleEngine([AmountDeviationRule(), UnusualHourRule(), HighRiskCategoryRule(), VelocityRule()])
print(eng.screen(txn, holder, []).explain())
"

# 5. Reconfigure the engine WITHOUT touching any rule class — composition in action
uv run python -c "
from rules import AmountDeviationRule, HighRiskCategoryRule
from engine import RuleEngine
strict = RuleEngine([AmountDeviationRule(alert_factor=4.0), HighRiskCategoryRule()], threshold=0.35)
print('rules:', [r.name for r in strict.rules], 'threshold:', strict.threshold)
"
