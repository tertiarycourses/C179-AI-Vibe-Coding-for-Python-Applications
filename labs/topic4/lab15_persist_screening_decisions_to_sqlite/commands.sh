#!/usr/bin/env bash
# Lab 15 — Persist Screening Decisions to SQLite
set -euo pipefail

# 3. Show why parameterised queries matter — the injection an f-string would allow
uv run python -c "
card = \"CH0001'; DROP TABLE screenings; --\"
print('UNSAFE would build:')
print(f\"  SELECT * FROM screenings WHERE card_ref = '{card}'\")
print('SAFE passes the value separately: con.execute(sql, (card,))')
"

# 5. Restart and post several transactions to build history
for amt in 86.40 5128.33 240.00 3900.00; do
  curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" \
    -d "{\"card_ref\":\"CH0001\",\"ts\":\"2026-04-15T02:30:00\",\"amount\":$amt,\"merchant_category\":\"electronics\",\"city\":\"Singapore\",\"lat\":1.3521,\"lon\":103.8198}" > /dev/null
done
curl -s http://127.0.0.1:8000/stats | python3 -m json.tool

# 6. Read the audit trail back
curl -s 'http://127.0.0.1:8000/screenings?limit=5' | python3 -m json.tool

# 7. Verify rollback works — a failed write must leave no partial row
uv run python -c "
import repository as repo
repo.init_schema()
before = len(repo.recent_screenings(1000))
try:
    with repo.connect() as con:
        con.execute('INSERT INTO screenings (card_ref,ts,amount,merchant_category,composite_score,decision,hits_json) VALUES (?,?,?,?,?,?,?)',
                    ('CH0001','2026-04-15T10:00:00',50.0,'grocery',0.1,'approve','[]'))
        raise RuntimeError('simulated failure after insert')
except RuntimeError as e:
    print('caught:', e)
after = len(repo.recent_screenings(1000))
print(f'rows before {before}, after {after} -> rolled back: {before == after}')
"
