# Lab 11 — Build Per-Cardholder Baselines with GroupBy

**Topic 3** · Compute per-group statistics with split-apply-combine

The learner computes each cardholder's own spending baseline and deviation for every transaction — the statistical foundation the AmountDeviationRule needs, done for 40 cardholders at once instead of one at a time.

- **You will build:** A per-cardholder baseline table and a deviation column on every transaction
- **Tools:** uv, pandas 3.0

## Steps

1. Compute one baseline per cardholder

   ```bash
   uv run python -c "
   from analytics import load_transactions
   df = load_transactions()
   base = df.groupby('card_ref')['amount'].agg(['count','mean','median','std']).round(2)
   print(base.head())
   print('cardholders:', len(base))
   "
   ```

2. Join each transaction to its cardholder baseline with transform — same shape as the original

   ```python
   # analytics.py (add)
   def add_deviation(df):
       """Attach each transaction's deviation from its own cardholder baseline."""
       df = df.copy()
       df["baseline"] = df.groupby("card_ref")["amount"].transform("median")
       df["dev_factor"] = (df["amount"] / df["baseline"]).round(2)
       return df
   ```

3. Find the biggest deviations and check them against the seeded fraud flag

   ```bash
   uv run python -c "
   from analytics import load_transactions, add_deviation
   df = add_deviation(load_transactions())
   top = df.nlargest(10, 'dev_factor')[['id','card_ref','amount','baseline','dev_factor','merchant_category','is_known_fraud']]
   print(top.to_string(index=False))
   print('\nof the top 10 deviations,', int(top.is_known_fraud.sum()), 'are seeded fraud')
   "
   ```

4. Measure how well deviation alone separates fraud from normal

   ```bash
   uv run python -c "
   from analytics import load_transactions, add_deviation
   df = add_deviation(load_transactions())
   print(df.groupby('is_known_fraud')['dev_factor'].describe().round(2)[['count','mean','50%','max']])
   "
   ```

5. Use median not mean for the baseline — prove why with an outlier

   ```bash
   uv run python -c "
   import pandas as pd
   s = pd.Series([100,110,95,105,20000])
   print('mean  ', round(s.mean(),2), '<- dragged up by the fraud itself')
   print('median', round(s.median(),2), '<- robust to the outlier')
   "
   ```

6. Note the analytics lesson: the statistic you choose changes what you can detect.

## Verify

Baselines compute for all 40 cardholders; dev_factor is attached to every row; the top deviations are dominated by seeded fraud; the learner can justify median over mean.
