#!/usr/bin/env bash
# Lab 12 — Detect Velocity Bursts with Rolling Time Windows
set -euo pipefail

# 2. Find the bursts
uv run python -c "
from analytics import load_transactions, add_velocity
df = add_velocity(load_transactions())
bursts = df[df.txn_count_10min >= 4]
print('burst transactions:', len(bursts))
print(bursts[['card_ref','ts','amount','merchant_category','txn_count_10min','is_known_fraud']].head(12).to_string(index=False))
"

# 3. Check the hit rate of velocity as a signal on its own
uv run python -c "
from analytics import load_transactions, add_velocity
df = add_velocity(load_transactions())
b = df[df.txn_count_10min >= 4]
print(f'{int(b.is_known_fraud.sum())} of {len(b)} burst transactions are seeded fraud')
print('precision:', round(100*b.is_known_fraud.mean(),1), '%')
"

# 4. Inspect one full burst to see the pattern a fraudster leaves
uv run python -c "
from analytics import load_transactions, add_velocity
df = add_velocity(load_transactions())
card = df[df.txn_count_10min >= 5].card_ref.iloc[0]
win = df[df.card_ref == card].nlargest(8, 'txn_count_10min')[['ts','amount','merchant_category','txn_count_10min']]
print(f'card {card}'); print(win.sort_values('ts').to_string(index=False))
"

# 6. Find the physically impossible journeys
uv run python -c "
from analytics import load_transactions, add_geo_velocity
df = add_geo_velocity(load_transactions())
imp = df[df.implied_kmh > 1000]
print('impossible journeys:', len(imp))
print(imp[['card_ref','ts','city','amount','implied_kmh','is_known_fraud']].to_string(index=False))
"
