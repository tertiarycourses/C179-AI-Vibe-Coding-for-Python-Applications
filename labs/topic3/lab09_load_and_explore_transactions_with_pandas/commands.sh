#!/usr/bin/env bash
# Lab 9 — Load and Explore Transactions with pandas
set -euo pipefail

# 1. Add pandas and load the table
uv add pandas
uv run python -c "
import sqlite3, pandas as pd
con = sqlite3.connect('cardguard.db')
df = pd.read_sql_query('SELECT * FROM transactions', con)
print(df.shape)
print(df.head())
"

# 2. Inspect dtypes — note ts arrived as text, not datetime
uv run python -c "
import sqlite3, pandas as pd
con = sqlite3.connect('cardguard.db')
df = pd.read_sql_query('SELECT * FROM transactions', con)
print(df.dtypes)
print(df.isna().sum())
"

# 4. Profile spend by merchant category — split-apply-combine
uv run python -c "
from analytics import load_transactions
df = load_transactions()
profile = (df.groupby('merchant_category', observed=True)['amount']
             .agg(['count', 'sum', 'mean', 'max']).round(2)
             .sort_values('sum', ascending=False))
print(profile)
"

# 5. Answer a real business question: which hours carry the most spend?
uv run python -c "
from analytics import load_transactions
df = load_transactions()
by_hour = df.groupby('hour')['amount'].agg(['count','sum']).round(2)
print(by_hour.tail(8))
print('\novernight share:', round(100*df[df.hour<6]['amount'].sum()/df['amount'].sum(),2), '%')
"

# 6. See the pandas 3.0 Copy-on-Write behaviour that AI assistants get wrong
uv run python -c "
import pandas as pd
df = pd.DataFrame({'a':[1,2,3],'b':[10,20,30]})
# The pandas 1.x idiom an assistant will often generate:
df[df.a > 1]['b'] = 0
print(df)   # unchanged under Copy-on-Write — the write went to a temporary
# The correct form:
df.loc[df.a > 1, 'b'] = 0
print(df)
"
