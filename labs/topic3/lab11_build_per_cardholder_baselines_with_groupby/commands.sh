#!/usr/bin/env bash
# Lab 11 — Build Per-Cardholder Baselines with GroupBy
set -euo pipefail

# 1. Compute one baseline per cardholder
uv run python -c "
from analytics import load_transactions
df = load_transactions()
base = df.groupby('card_ref')['amount'].agg(['count','mean','median','std']).round(2)
print(base.head())
print('cardholders:', len(base))
"

# 3. Find the biggest deviations and check them against the seeded fraud flag
uv run python -c "
from analytics import load_transactions, add_deviation
df = add_deviation(load_transactions())
top = df.nlargest(10, 'dev_factor')[['id','card_ref','amount','baseline','dev_factor','merchant_category','is_known_fraud']]
print(top.to_string(index=False))
print('\nof the top 10 deviations,', int(top.is_known_fraud.sum()), 'are seeded fraud')
"

# 4. Measure how well deviation alone separates fraud from normal
uv run python -c "
from analytics import load_transactions, add_deviation
df = add_deviation(load_transactions())
print(df.groupby('is_known_fraud')['dev_factor'].describe().round(2)[['count','mean','50%','max']])
"

# 5. Use median not mean for the baseline — prove why with an outlier
uv run python -c "
import pandas as pd
s = pd.Series([100,110,95,105,20000])
print('mean  ', round(s.mean(),2), '<- dragged up by the fraud itself')
print('median', round(s.median(),2), '<- robust to the outlier')
"
