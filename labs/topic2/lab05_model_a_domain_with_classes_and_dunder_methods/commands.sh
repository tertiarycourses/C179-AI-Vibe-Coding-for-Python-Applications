#!/usr/bin/env bash
# Lab 5 — Model a Domain with Classes and Dunder Methods
set -euo pipefail

# 1. Start the project and generate the database
uv init cardguard
cd cardguard
uv add pandas
cp ../mockdata.py .
uv run python mockdata.py

# 2. Look at the raw shape of the data you are about to model
uv run python -c "
import sqlite3
con = sqlite3.connect('cardguard.db')
row = con.execute('SELECT * FROM transactions LIMIT 1').fetchone()
print(row)
"

# 5. Load real rows through the class and print them
uv run python -c "
import sqlite3
from models import Transaction
con = sqlite3.connect('cardguard.db')
rows = con.execute('SELECT * FROM transactions LIMIT 5').fetchall()
for r in rows:
    t = Transaction.from_row(r)
    print(t, '| hour', t.hour, '| high risk', t.is_high_risk_category)
"

# 6. Verify @dataclass gave you equality for free — dicts compare by content, objects normally by identity
uv run python -c "
from datetime import datetime
from models import Transaction
a = Transaction(1, 'CH0001', datetime(2026,4,1,9), 50.0, 'grocery', 'Singapore', 1.35, 103.8)
b = Transaction(1, 'CH0001', datetime(2026,4,1,9), 50.0, 'grocery', 'Singapore', 1.35, 103.8)
print('equal:', a == b)
print('same object:', a is b)
"
