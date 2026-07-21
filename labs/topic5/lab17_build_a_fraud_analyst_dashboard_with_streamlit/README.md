# Lab 17 — Build a Fraud Analyst Dashboard with Streamlit

**Topic 5** · Create a data application UI that consumes the API

The learner builds the third tier: a Streamlit dashboard a fraud analyst actually uses — review queue, screening form and trend charts — calling the FastAPI service rather than reaching into the database.

- **You will build:** A running Streamlit dashboard with live screening, a review queue and charts
- **Tools:** uv, Streamlit, FastAPI, httpx, pandas

## Steps

1. Add Streamlit

   ```bash
   uv add streamlit httpx
   ```

2. Build the dashboard shell and the live screening form

   ```python
   # app.py
   import httpx
   import pandas as pd
   import streamlit as st
   
   API = st.secrets.get("api_url", "http://127.0.0.1:8000")
   
   st.set_page_config(page_title="CardGuard", page_icon="\U0001F6E1", layout="wide")
   st.title("CardGuard — Fraud Screening Console")
   
   with st.sidebar:
       st.header("Screen a transaction")
       card_ref = st.text_input("Card reference", "CH0001")
       amount = st.number_input("Amount (SGD)", min_value=0.01, value=86.40, step=10.0)
       category = st.selectbox("Merchant category",
           ["grocery","fuel","restaurant","electronics","online_gaming",
            "jewellery","crypto_exchange","gift_cards","pharmacy","transport"])
       hour = st.slider("Hour of day", 0, 23, 10)
       submitted = st.button("Screen", type="primary")
   
   if submitted:
       payload = {"card_ref": card_ref, "ts": f"2026-04-15T{hour:02d}:30:00",
                  "amount": float(amount), "merchant_category": category,
                  "city": "Singapore", "lat": 1.3521, "lon": 103.8198}
       try:
           r = httpx.post(f"{API}/screen", json=payload, timeout=10)
           r.raise_for_status()
           out = r.json()
       except httpx.HTTPStatusError as exc:
           st.error(f"API rejected the request ({exc.response.status_code}): {exc.response.text}")
       except httpx.RequestError:
           st.error("Cannot reach the screening API. Is it running on port 8000?")
       else:
           colour = {"approve": "green", "review": "orange", "decline": "red"}[out["decision"]]
           st.markdown(f"### Decision: :{colour}[{out['decision'].upper()}]")
           st.metric("Composite score", out["composite_score"])
           if out["hits"]:
               st.dataframe(pd.DataFrame(out["hits"]), width="stretch")
           else:
               st.info("No rule fired on this transaction.")
   ```

3. Add the review queue and trend charts

   ```python
   # app.py (add)
   st.divider()
   left, right = st.columns([2, 1])
   
   try:
       rows = httpx.get(f"{API}/screenings", params={"limit": 200}, timeout=10).json()
       stats = httpx.get(f"{API}/stats", timeout=10).json()
   except httpx.RequestError:
       st.warning("API unavailable — showing no history.")
       rows, stats = [], {}
   
   with left:
       st.subheader("Recent screenings")
       if rows:
           df = pd.DataFrame(rows)
           df["screened_at"] = pd.to_datetime(df["screened_at"])
           st.dataframe(
               df[["card_ref","amount","merchant_category","composite_score","decision","screened_at"]],
               width="stretch", height=340)
       else:
           st.info("No screenings yet — submit one from the sidebar.")
   
   with right:
       st.subheader("Decisions")
       if stats:
           st.bar_chart(pd.Series(stats, name="count"))
           total = sum(stats.values())
           flagged = stats.get("review", 0) + stats.get("decline", 0)
           st.metric("Flag rate", f"{100 * flagged / total:.1f}%" if total else "—")
   ```

4. Run both tiers — API in one terminal, UI in another

   ```python
   # terminal 1
   uv run uvicorn main:app --reload --port 8000
   
   # terminal 2
   uv run streamlit run app.py
   ```

5. Screen a normal transaction in the UI and watch it land in the queue

   ```bash
   open http://localhost:8501
   ```

6. Screen a $5,000 jewellery charge at 02:00 and confirm it turns red
7. Stop the API and confirm the UI degrades gracefully instead of crashing

   ```python
   # stop uvicorn (Ctrl-C), then click Screen in the UI
   ```

8. Note the architecture: the UI never touches SQLite. Swapping the database would not change app.py at all.

## Verify

The dashboard screens transactions live, colour-codes decisions, lists the review queue and charts decision counts; with the API stopped it shows a clear error rather than a traceback.
