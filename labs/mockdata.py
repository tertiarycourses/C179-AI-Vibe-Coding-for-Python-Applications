"""
Deterministic mock data generator for the CardGuard fraud-detection labs.

Seeded so every learner and the trainer see IDENTICAL numbers. No real
cardholder data is used or required. Run:

    uv run python mockdata.py

Produces cardguard.db (SQLite) with `cardholders` and `transactions`.
"""

import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

SEED = 42
DB_PATH = Path("cardguard.db")

MERCHANT_CATEGORIES = [
    ("grocery", 0.001), ("fuel", 0.002), ("restaurant", 0.002),
    ("electronics", 0.010), ("online_gaming", 0.020),
    ("jewellery", 0.025), ("crypto_exchange", 0.040),
    ("gift_cards", 0.035), ("pharmacy", 0.001), ("transport", 0.001),
]

CITIES = [
    ("Singapore", 1.3521, 103.8198), ("Kuala Lumpur", 3.1390, 101.6869),
    ("Jakarta", -6.2088, 106.8456), ("Bangkok", 13.7563, 100.5018),
    ("Hong Kong", 22.3193, 114.1694), ("Sydney", -33.8688, 151.2093),
    ("London", 51.5074, -0.1278), ("New York", 40.7128, -74.0060),
]

FIRST = ["Aisha", "Bala", "Chen", "Divya", "Eng", "Farid", "Grace", "Hakim",
         "Indra", "Jia", "Kamal", "Lina", "Meera", "Nadia", "Omar", "Priya"]
LAST = ["Tan", "Lim", "Kumar", "Wong", "Rahman", "Chua", "Devi", "Ng",
        "Ismail", "Goh", "Menon", "Yeo"]


def make_cardholders(rng, n=40):
    rows = []
    for i in range(1, n + 1):
        name = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        home = rng.choice(CITIES)
        typical = round(rng.uniform(35, 220), 2)
        rows.append((i, f"CH{i:04d}", name, home[0], typical,
                     rng.choice([7, 8, 9, 10]), rng.choice([21, 22, 23])))
    return rows


def make_transactions(rng, cardholders, days=60, per_day=(2, 7)):
    """Normal spend, then deliberately seeded fraud patterns."""
    rows = []
    tid = 0
    start = datetime(2026, 4, 1, 0, 0, 0)
    city_by_name = {c[0]: c for c in CITIES}

    for ch in cardholders:
        ch_id, card_ref, _name, home_city, typical, wake, sleep = ch
        home = city_by_name[home_city]
        for d in range(days):
            for _ in range(rng.randint(*per_day)):
                tid += 1
                hour = rng.randint(wake, sleep)
                ts = start + timedelta(days=d, hours=hour,
                                       minutes=rng.randint(0, 59))
                amount = round(max(1.0, rng.gauss(typical, typical * 0.35)), 2)
                cat = rng.choices([c[0] for c in MERCHANT_CATEGORIES],
                                  weights=[8, 6, 7, 2, 1, 1, 1, 1, 3, 5])[0]
                rows.append((tid, card_ref, ts.isoformat(timespec="seconds"),
                             amount, cat, home[0], home[1], home[2], 0))

    # ---- seeded fraud pattern 1: velocity burst (6 txns in ~4 minutes)
    for ch in rng.sample(cardholders, 4):
        card_ref, typical = ch[1], ch[4]
        base = start + timedelta(days=rng.randint(10, 50), hours=2)
        for k in range(6):
            tid += 1
            ts = base + timedelta(seconds=45 * k)
            rows.append((tid, card_ref, ts.isoformat(timespec="seconds"),
                         round(typical * rng.uniform(0.8, 1.4), 2),
                         "online_gaming", "Singapore", 1.3521, 103.8198, 1))

    # ---- seeded fraud pattern 2: amount spike (18-30x the cardholder norm)
    for ch in rng.sample(cardholders, 5):
        card_ref, typical = ch[1], ch[4]
        tid += 1
        ts = start + timedelta(days=rng.randint(10, 50), hours=rng.randint(1, 5))
        rows.append((tid, card_ref, ts.isoformat(timespec="seconds"),
                     round(typical * rng.uniform(18, 30), 2),
                     rng.choice(["jewellery", "electronics"]),
                     "Singapore", 1.3521, 103.8198, 1))

    # ---- seeded fraud pattern 3: geographic impossibility
    for ch in rng.sample(cardholders, 4):
        card_ref, typical = ch[1], ch[4]
        base = start + timedelta(days=rng.randint(10, 50), hours=13)
        tid += 1
        rows.append((tid, card_ref, base.isoformat(timespec="seconds"),
                     round(typical, 2), "restaurant",
                     "Singapore", 1.3521, 103.8198, 1))
        far = city_by_name["London"]
        tid += 1
        rows.append((tid, card_ref,
                     (base + timedelta(minutes=40)).isoformat(timespec="seconds"),
                     round(typical * 3, 2), "electronics",
                     far[0], far[1], far[2], 1))

    # ---- seeded fraud pattern 4: high-risk category at an unusual hour
    for ch in rng.sample(cardholders, 5):
        card_ref, typical = ch[1], ch[4]
        tid += 1
        ts = start + timedelta(days=rng.randint(10, 50), hours=rng.choice([3, 4]))
        rows.append((tid, card_ref, ts.isoformat(timespec="seconds"),
                     round(typical * rng.uniform(4, 9), 2),
                     rng.choice(["crypto_exchange", "gift_cards"]),
                     "Singapore", 1.3521, 103.8198, 1))

    rows.sort(key=lambda r: r[2])
    return rows


def build(db_path: Path = DB_PATH) -> None:
    rng = random.Random(SEED)
    cardholders = make_cardholders(rng)
    transactions = make_transactions(rng, cardholders)

    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    con.execute("""
        CREATE TABLE cardholders (
            id INTEGER PRIMARY KEY, card_ref TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL, home_city TEXT NOT NULL,
            typical_amount REAL NOT NULL,
            wake_hour INTEGER NOT NULL, sleep_hour INTEGER NOT NULL)""")
    con.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY, card_ref TEXT NOT NULL,
            ts TEXT NOT NULL, amount REAL NOT NULL,
            merchant_category TEXT NOT NULL, city TEXT NOT NULL,
            lat REAL NOT NULL, lon REAL NOT NULL,
            is_known_fraud INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (card_ref) REFERENCES cardholders(card_ref))""")
    con.execute("CREATE INDEX idx_txn_card ON transactions(card_ref, ts)")
    con.executemany("INSERT INTO cardholders VALUES (?,?,?,?,?,?,?)", cardholders)
    con.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)", transactions)
    con.commit()

    n_fraud = sum(1 for r in transactions if r[8] == 1)
    print(f"Wrote {db_path}")
    print(f"  cardholders : {len(cardholders)}")
    print(f"  transactions: {len(transactions)}")
    print(f"  seeded fraud: {n_fraud}")
    con.close()


if __name__ == "__main__":
    build()
