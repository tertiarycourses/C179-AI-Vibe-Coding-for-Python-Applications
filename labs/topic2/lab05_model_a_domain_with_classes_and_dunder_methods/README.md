# Lab 5 — Model a Domain with Classes and Dunder Methods

**Topic 2** · Define classes that bundle data with behaviour

The learner replaces loose dictionaries with a Transaction class, adds __init__, __repr__ and __eq__, and sees why a class is easier to reason about than a dict once behaviour is attached to the data.

- **You will build:** A Transaction class with construction, printing, equality and derived properties
- **Tools:** uv, Python 3.12, dataclasses, sqlite3

## Steps

1. Start the project and generate the database

   ```bash
   uv init cardguard
   cd cardguard
   uv add pandas
   cp ../mockdata.py .
   uv run python mockdata.py
   ```

2. Look at the raw shape of the data you are about to model

   ```bash
   uv run python -c "
   import sqlite3
   con = sqlite3.connect('cardguard.db')
   row = con.execute('SELECT * FROM transactions LIMIT 1').fetchone()
   print(row)
   "
   ```

3. Write the Transaction class — data and the behaviour that belongs with it

   ```python
   # models.py
   from dataclasses import dataclass
   from datetime import datetime
   
   @dataclass
   class Transaction:
       """One card transaction presented for screening."""
       id: int
       card_ref: str
       ts: datetime
       amount: float
       merchant_category: str
       city: str
       lat: float
       lon: float
   
       @property
       def hour(self) -> int:
           """Hour of day, 0-23 — used by the unusual-hour rule."""
           return self.ts.hour
   
       @property
       def is_high_risk_category(self) -> bool:
           return self.merchant_category in {"crypto_exchange", "gift_cards", "jewellery"}
   
       def __repr__(self) -> str:
           return (f"Transaction(id={self.id}, card={self.card_ref}, "
                   f"${self.amount:,.2f}, {self.merchant_category}, {self.city})")
   ```

4. Add a constructor that builds a Transaction from a database row

   ```python
       @classmethod
       def from_row(cls, row: tuple) -> "Transaction":
           """Build a Transaction from a sqlite row tuple."""
           return cls(id=row[0], card_ref=row[1], ts=datetime.fromisoformat(row[2]),
                      amount=row[3], merchant_category=row[4], city=row[5],
                      lat=row[6], lon=row[7])
   ```

5. Load real rows through the class and print them

   ```bash
   uv run python -c "
   import sqlite3
   from models import Transaction
   con = sqlite3.connect('cardguard.db')
   rows = con.execute('SELECT * FROM transactions LIMIT 5').fetchall()
   for r in rows:
       t = Transaction.from_row(r)
       print(t, '| hour', t.hour, '| high risk', t.is_high_risk_category)
   "
   ```

6. Verify @dataclass gave you equality for free — dicts compare by content, objects normally by identity

   ```bash
   uv run python -c "
   from datetime import datetime
   from models import Transaction
   a = Transaction(1, 'CH0001', datetime(2026,4,1,9), 50.0, 'grocery', 'Singapore', 1.35, 103.8)
   b = Transaction(1, 'CH0001', datetime(2026,4,1,9), 50.0, 'grocery', 'Singapore', 1.35, 103.8)
   print('equal:', a == b)
   print('same object:', a is b)
   "
   ```

7. Note the gain: hour and is_high_risk_category live WITH the data. With dicts, that logic would be scattered across every caller.

## Verify

Transaction.from_row builds objects from the database, __repr__ prints readably, __eq__ compares by value, and the derived properties return correct results.
