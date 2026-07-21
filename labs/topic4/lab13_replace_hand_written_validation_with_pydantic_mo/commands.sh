#!/usr/bin/env bash
# Lab 13 — Replace Hand-Written Validation with Pydantic Models
set -euo pipefail

# 1. Add Pydantic to the project
uv add pydantic

# 3. Compare against Topic 3 — one model replaces the whole hand-written validator
uv run python -c "
from schemas import TransactionIn
good = TransactionIn(card_ref='CH0001', ts='2026-04-15T02:14:00', amount=4820.50,
                     merchant_category='jewellery', city='singapore', lat=1.3521, lon=103.8198)
print(good)
print('city normalised to:', good.city)
print('ts coerced to:', type(good.ts).__name__)
"

# 4. Read a validation failure — Pydantic reports EVERY problem, not just the first
uv run python -c "
from pydantic import ValidationError
from schemas import TransactionIn
try:
    TransactionIn(card_ref='BAD', ts='not-a-date', amount=-5,
                  merchant_category='casino', city='X', lat=999, lon=0)
except ValidationError as e:
    for err in e.errors():
        print(f\"  {'.'.join(str(x) for x in err['loc']):<20} {err['msg']}\")
"

# 6. Serialise to JSON — the wire format comes free
uv run python -c "
from schemas import ScreeningOut, RuleHit
out = ScreeningOut(card_ref='CH0023', composite_score=0.933, flagged=True, decision='decline',
                   hits=[RuleHit(rule_name='AmountDeviationRule', score=1.0, reason='26.89x baseline'),
                         RuleHit(rule_name='UnusualHourRule', score=0.8, reason='02:00')])
print(out.model_dump_json(indent=2))
"

# 7. Load real database rows THROUGH the model to catch any dirty data
uv run python -c "
import sqlite3
from pydantic import ValidationError
from schemas import TransactionIn
con = sqlite3.connect('cardguard.db')
con.row_factory = sqlite3.Row
ok = bad = 0
for r in con.execute('SELECT * FROM transactions LIMIT 500'):
    try:
        TransactionIn(**{k: r[k] for k in ('card_ref','ts','amount','merchant_category','city','lat','lon')})
        ok += 1
    except ValidationError:
        bad += 1
print(f'validated {ok}, rejected {bad}')
"
