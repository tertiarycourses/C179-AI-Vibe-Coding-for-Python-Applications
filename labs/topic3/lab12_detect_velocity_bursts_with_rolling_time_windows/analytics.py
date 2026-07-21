# analytics.py (add)
def add_velocity(df, window: str = "10min"):
    """Count transactions per cardholder inside a rolling time window."""
    df = df.sort_values(["card_ref", "ts"]).copy()
    counts = (df.set_index("ts")
                .groupby("card_ref")["amount"]
                .rolling(window).count()
                .reset_index(name="txn_count_10min"))
    df = df.merge(counts, on=["card_ref", "ts"], how="left")
    return df

# analytics.py (add)
import numpy as np

def add_geo_velocity(df):
    """Implied travel speed (km/h) between consecutive transactions."""
    df = df.sort_values(["card_ref", "ts"]).copy()
    g = df.groupby("card_ref")
    lat1, lon1 = np.radians(g["lat"].shift()), np.radians(g["lon"].shift())
    lat2, lon2 = np.radians(df["lat"]), np.radians(df["lon"])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    km = 6371 * 2 * np.arcsin(np.sqrt(a))
    hours = g["ts"].diff().dt.total_seconds() / 3600
    df["implied_kmh"] = (km / hours.replace(0, np.nan)).round(1)
    return df

