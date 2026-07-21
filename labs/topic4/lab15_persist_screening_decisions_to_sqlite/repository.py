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

