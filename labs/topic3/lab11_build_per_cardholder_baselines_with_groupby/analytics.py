# analytics.py (add)
def add_deviation(df):
    """Attach each transaction's deviation from its own cardholder baseline."""
    df = df.copy()
    df["baseline"] = df.groupby("card_ref")["amount"].transform("median")
    df["dev_factor"] = (df["amount"] / df["baseline"]).round(2)
    return df

