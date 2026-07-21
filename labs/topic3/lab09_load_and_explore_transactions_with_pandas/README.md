# Lab 9 — Load and Explore Transactions with pandas

**Topic 3** · Read SQL into a DataFrame and profile it

The learner loads the transaction table into pandas, inspects dtypes and null counts, and produces a first profile of spending — the step every analytics task starts with.

- **You will build:** A loaded, correctly-typed transactions DataFrame plus a spend profile by category
- **Tools:** uv, pandas 3.0, sqlite3

## Steps

1. Add pandas and load the table

   ```bash
   uv add pandas
   uv run python -c "
   import sqlite3, pandas as pd
   con = sqlite3.connect('cardguard.db')
   df = pd.read_sql_query('SELECT * FROM transactions', con)
   print(df.shape)
   print(df.head())
   "
   ```

2. Inspect dtypes — note ts arrived as text, not datetime

   ```bash
   uv run python -c "
   import sqlite3, pandas as pd
   con = sqlite3.connect('cardguard.db')
   df = pd.read_sql_query('SELECT * FROM transactions', con)
   print(df.dtypes)
   print(df.isna().sum())
   "
   ```

3. Write a loader that fixes the types once, so no downstream code has to

   ```python
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
   ```

4. Profile spend by merchant category — split-apply-combine

   ```bash
   uv run python -c "
   from analytics import load_transactions
   df = load_transactions()
   profile = (df.groupby('merchant_category', observed=True)['amount']
                .agg(['count', 'sum', 'mean', 'max']).round(2)
                .sort_values('sum', ascending=False))
   print(profile)
   "
   ```

5. Answer a real business question: which hours carry the most spend?

   ```bash
   uv run python -c "
   from analytics import load_transactions
   df = load_transactions()
   by_hour = df.groupby('hour')['amount'].agg(['count','sum']).round(2)
   print(by_hour.tail(8))
   print('\novernight share:', round(100*df[df.hour<6]['amount'].sum()/df['amount'].sum(),2), '%')
   "
   ```

6. See the pandas 3.0 Copy-on-Write behaviour that AI assistants get wrong

   ```bash
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
   ```

7. Note the lesson: verify generated pandas against your installed version, not against a tutorial.

## Verify

load_transactions returns 10,851 rows with ts as datetime64; the category profile and hourly breakdown print; the learner can state why chained assignment silently fails.
