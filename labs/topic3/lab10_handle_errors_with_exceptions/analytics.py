# analytics.py (updated)
import sqlite3
from pathlib import Path
import pandas as pd
from errors import DataSourceError

def load_transactions(db_path: str = "cardguard.db") -> pd.DataFrame:
    """Load transactions, raising DataSourceError on any read failure."""
    if not Path(db_path).exists():
        raise DataSourceError(f"database not found: {db_path}")
    con = None
    try:
        con = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM transactions", con)
    except sqlite3.DatabaseError as exc:
        raise DataSourceError(f"could not read {db_path}: {exc}") from exc
    else:
        df["ts"] = pd.to_datetime(df["ts"])
        df["hour"] = df["ts"].dt.hour
        return df
    finally:
        if con is not None:
            con.close()      # runs on success AND on failure

