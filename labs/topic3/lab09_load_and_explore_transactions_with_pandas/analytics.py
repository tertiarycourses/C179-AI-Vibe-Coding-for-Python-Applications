# analytics.py
import sqlite3
import pandas as pd

def load_transactions(db_path: str = "cardguard.db") -> pd.DataFrame:
    """Load transactions with correct dtypes."""
    con = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM transactions", con)
    finally:
        con.close()          # always closes, even if the query raises
    df["ts"] = pd.to_datetime(df["ts"])
    df["merchant_category"] = df["merchant_category"].astype("category")
    df["hour"] = df["ts"].dt.hour
    df["date"] = df["ts"].dt.date
    return df

