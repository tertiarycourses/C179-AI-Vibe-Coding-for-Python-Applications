#!/usr/bin/env bash
# Lab 6 — Encapsulate State with Properties and Validation
set -euo pipefail

# 3. Prove the baseline cannot be overwritten from outside
uv run python -c "
from cardholder import Cardholder
ch = Cardholder('CH0001', 'Aisha Tan', 'Singapore', 120.0)
try:
    ch.typical_amount = 999999
except AttributeError as e:
    print('blocked:', e)
"

# 4. Drive the baseline the sanctioned way and watch it move
uv run python -c "
from cardholder import Cardholder
ch = Cardholder('CH0001', 'Aisha Tan', 'Singapore', 120.0)
for amt in [110, 130, 125, 118, 122]:
    ch.observe(amt)
print('baseline', ch.typical_amount, 'after', ch.observed_count, 'observations')
print('a $2,400 charge is', ch.deviation_factor(2400), 'x baseline')
"

# 5. Confirm validation rejects bad input at both entry points
uv run python -c "
from cardholder import Cardholder
for bad in [lambda: Cardholder('C','n','SG',0), lambda: Cardholder('C','n','SG',120).observe(-5)]:
    try:
        bad(); print('NOT CAUGHT')
    except ValueError as e:
        print('correctly raised:', e)
"

# 6. Load the real cardholders and rank them by baseline
uv run python -c "
import sqlite3
from cardholder import Cardholder
con = sqlite3.connect('cardguard.db')
rows = con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders').fetchall()
chs = [Cardholder(*r) for r in rows]
top = sorted(chs, key=lambda c: c.typical_amount, reverse=True)[:5]
for c in top:
    print(f'{c.card_ref} {c.name:<16} baseline ${c.typical_amount:,.2f}')
"
