# Lab 15 — Persist Screening Decisions to SQLite

**Topic 4** · Write application state to a database from the API layer

The learner adds a repository layer that records every screening decision, so the service builds an audit trail — a regulatory requirement for real fraud systems, and the data the Topic 5 dashboard reads.

- **You will build:** A screenings table plus a repository module with save and query functions
- **Tools:** uv, sqlite3, FastAPI

## Steps

1. Create the audit table

   ```python
   # repository.py
   import sqlite3
   import json
   from contextlib import contextmanager
   from pathlib import Path
   
   DB = "cardguard.db"
   
   @contextmanager
   def connect(db_path: str = DB):
       """Connection that always commits or rolls back, and always closes."""
       con = sqlite3.connect(db_path)
       con.row_factory = sqlite3.Row
       try:
           yield con
           con.commit()
       except Exception:
           con.rollback()
           raise
       finally:
           con.close()
   
   def init_schema(db_path: str = DB) -> None:
       with connect(db_path) as con:
           con.execute("""
               CREATE TABLE IF NOT EXISTS screenings (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   card_ref TEXT NOT NULL,
                   ts TEXT NOT NULL,
                   amount REAL NOT NULL,
                   merchant_category TEXT NOT NULL,
                   composite_score REAL NOT NULL,
                   decision TEXT NOT NULL,
                   hits_json TEXT NOT NULL,
                   screened_at TEXT NOT NULL DEFAULT (datetime('now')))""")
           con.execute("CREATE INDEX IF NOT EXISTS idx_scr_card ON screenings(card_ref)")
   ```

2. Add save and query functions — parameterised, never string-formatted

   ```python
   # repository.py (add)
   def save_screening(txn_in, result, db_path: str = DB) -> int:
       """Record one decision; returns the new row id."""
       with connect(db_path) as con:
           cur = con.execute(
               "INSERT INTO screenings (card_ref, ts, amount, merchant_category,"
               " composite_score, decision, hits_json) VALUES (?,?,?,?,?,?,?)",
               (txn_in.card_ref, txn_in.ts.isoformat(), txn_in.amount,
                txn_in.merchant_category, result.composite_score, result.decision,
                json.dumps([h.model_dump() for h in result.hits])))
           return cur.lastrowid
   
   def recent_screenings(limit: int = 20, db_path: str = DB) -> list[dict]:
       with connect(db_path) as con:
           rows = con.execute(
               "SELECT * FROM screenings ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
       return [dict(r) for r in rows]
   
   def decision_counts(db_path: str = DB) -> dict[str, int]:
       with connect(db_path) as con:
           rows = con.execute(
               "SELECT decision, COUNT(*) n FROM screenings GROUP BY decision").fetchall()
       return {r["decision"]: r["n"] for r in rows}
   ```

3. Show why parameterised queries matter — the injection an f-string would allow

   ```bash
   uv run python -c "
   card = \"CH0001'; DROP TABLE screenings; --\"
   print('UNSAFE would build:')
   print(f\"  SELECT * FROM screenings WHERE card_ref = '{card}'\")
   print('SAFE passes the value separately: con.execute(sql, (card,))')
   "
   ```

4. Wire persistence into the endpoint

   ```python
   # main.py (add)
   from repository import init_schema, save_screening, recent_screenings, decision_counts
   
   @app.on_event("startup")
   def _startup() -> None:
       init_schema()
   
   # inside screen(), just before returning:
   #     save_screening(txn_in, out)
   
   @app.get("/screenings")
   def list_screenings(limit: int = 20) -> list[dict]:
       """Recent decisions, newest first — the audit trail."""
       return recent_screenings(limit)
   
   @app.get("/stats")
   def stats() -> dict:
       """Decision counts for the dashboard."""
       return decision_counts()
   ```

5. Restart and post several transactions to build history

   ```bash
   for amt in 86.40 5128.33 240.00 3900.00; do
     curl -s -X POST http://127.0.0.1:8000/screen -H "Content-Type: application/json" \
       -d "{\"card_ref\":\"CH0001\",\"ts\":\"2026-04-15T02:30:00\",\"amount\":$amt,\"merchant_category\":\"electronics\",\"city\":\"Singapore\",\"lat\":1.3521,\"lon\":103.8198}" > /dev/null
   done
   curl -s http://127.0.0.1:8000/stats | python3 -m json.tool
   ```

6. Read the audit trail back

   ```bash
   curl -s 'http://127.0.0.1:8000/screenings?limit=5' | python3 -m json.tool
   ```

7. Verify rollback works — a failed write must leave no partial row

   ```bash
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
   ```


## Verify

Screenings persist and are queryable via /screenings and /stats; the injection demo shows why parameters are used; the rollback test proves the row count is unchanged after a mid-transaction failure.
