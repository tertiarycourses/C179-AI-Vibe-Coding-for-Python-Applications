# main.py (add)
from repository import init_schema, save_screening, recent_screenings, decision_counts

@app.on_event("startup")
def _startup() -> None:
    init_schema()

# inside screen(), just before returning:
#     save_screening(txn_in, out)

@app.get("/screenings")
def list_screenings(limit: int = 20) -> list[dict]:
    """Recent decisions, newest first — the audit trail."""
    return recent_screenings(limit)

@app.get("/stats")
def stats() -> dict:
    """Decision counts for the dashboard."""
    return decision_counts()

