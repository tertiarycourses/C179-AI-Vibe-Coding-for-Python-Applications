# Lab 12 — Detect Velocity Bursts with Rolling Time Windows

**Topic 3** · Analyse ordered time-series data per group

The learner sorts transactions per cardholder and counts how many occur inside a rolling 10-minute window — the history the VelocityRule needs, which cannot be computed one transaction at a time.

- **You will build:** A txn_count_10min column plus the burst transactions it exposes
- **Tools:** uv, pandas 3.0, rolling windows

## Steps

1. Sort by cardholder and time — order is a precondition for any window function

   ```python
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
   ```

2. Find the bursts

   ```bash
   uv run python -c "
   from analytics import load_transactions, add_velocity
   df = add_velocity(load_transactions())
   bursts = df[df.txn_count_10min >= 4]
   print('burst transactions:', len(bursts))
   print(bursts[['card_ref','ts','amount','merchant_category','txn_count_10min','is_known_fraud']].head(12).to_string(index=False))
   "
   ```

3. Check the hit rate of velocity as a signal on its own

   ```bash
   uv run python -c "
   from analytics import load_transactions, add_velocity
   df = add_velocity(load_transactions())
   b = df[df.txn_count_10min >= 4]
   print(f'{int(b.is_known_fraud.sum())} of {len(b)} burst transactions are seeded fraud')
   print('precision:', round(100*b.is_known_fraud.mean(),1), '%')
   "
   ```

4. Inspect one full burst to see the pattern a fraudster leaves

   ```bash
   uv run python -c "
   from analytics import load_transactions, add_velocity
   df = add_velocity(load_transactions())
   card = df[df.txn_count_10min >= 5].card_ref.iloc[0]
   win = df[df.card_ref == card].nlargest(8, 'txn_count_10min')[['ts','amount','merchant_category','txn_count_10min']]
   print(f'card {card}'); print(win.sort_values('ts').to_string(index=False))
   "
   ```

5. Compute the geographic-impossibility signal the engine is still missing

   ```python
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
   ```

6. Find the physically impossible journeys

   ```bash
   uv run python -c "
   from analytics import load_transactions, add_geo_velocity
   df = add_geo_velocity(load_transactions())
   imp = df[df.implied_kmh > 1000]
   print('impossible journeys:', len(imp))
   print(imp[['card_ref','ts','city','amount','implied_kmh','is_known_fraud']].to_string(index=False))
   "
   ```

7. Note: velocity and geography are only visible ACROSS rows. Row-at-a-time scoring cannot see them.

## Verify

Velocity bursts and impossible journeys are both detected, dominated by seeded fraud, and the learner can explain why these signals require sorted per-group windows.
