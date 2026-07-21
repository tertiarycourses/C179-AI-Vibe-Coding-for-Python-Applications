# Lab 13 — Replace Hand-Written Validation with Pydantic Models

**Topic 4** · Declare data shape with type hints and validate at runtime

The learner replaces the manual validate_txn() from Topic 3 with a Pydantic model, getting type coercion, field constraints and structured error reporting for free — far less code, far better errors.

- **You will build:** TransactionIn and ScreeningOut Pydantic models with field constraints
- **Tools:** uv, Pydantic v2

## Steps

1. Add Pydantic to the project

   ```bash
   uv add pydantic
   ```

2. Declare the model — the constraints ARE the validation

   ```python
   # schemas.py
   from datetime import datetime
   from typing import Literal
   from pydantic import BaseModel, Field, field_validator
   
   CATEGORIES = Literal["grocery","fuel","restaurant","electronics","online_gaming",
                        "jewellery","crypto_exchange","gift_cards","pharmacy","transport"]
   
   class TransactionIn(BaseModel):
       """One transaction submitted for screening."""
       card_ref: str = Field(pattern=r"^CH\d{4}$", description="Cardholder reference")
       ts: datetime
       amount: float = Field(gt=0, le=1_000_000, description="Charge amount in SGD")
       merchant_category: CATEGORIES
       city: str = Field(min_length=2, max_length=64)
       lat: float = Field(ge=-90, le=90)
       lon: float = Field(ge=-180, le=180)
   
       @field_validator("city")
       @classmethod
       def title_case_city(cls, v: str) -> str:
           return v.strip().title()
   ```

3. Compare against Topic 3 — one model replaces the whole hand-written validator

   ```bash
   uv run python -c "
   from schemas import TransactionIn
   good = TransactionIn(card_ref='CH0001', ts='2026-04-15T02:14:00', amount=4820.50,
                        merchant_category='jewellery', city='singapore', lat=1.3521, lon=103.8198)
   print(good)
   print('city normalised to:', good.city)
   print('ts coerced to:', type(good.ts).__name__)
   "
   ```

4. Read a validation failure — Pydantic reports EVERY problem, not just the first

   ```bash
   uv run python -c "
   from pydantic import ValidationError
   from schemas import TransactionIn
   try:
       TransactionIn(card_ref='BAD', ts='not-a-date', amount=-5,
                     merchant_category='casino', city='X', lat=999, lon=0)
   except ValidationError as e:
       for err in e.errors():
           print(f\"  {'.'.join(str(x) for x in err['loc']):<20} {err['msg']}\")
   "
   ```

5. Define the response model separately — request and response are different contracts

   ```python
   # schemas.py (add)
   class RuleHit(BaseModel):
       rule_name: str
       score: float = Field(ge=0, le=1)
       reason: str
   
   class ScreeningOut(BaseModel):
       """What the screening service returns."""
       card_ref: str
       composite_score: float = Field(ge=0, le=1)
       flagged: bool
       decision: Literal["approve", "review", "decline"]
       hits: list[RuleHit] = []
       errors: list[str] = []
   ```

6. Serialise to JSON — the wire format comes free

   ```bash
   uv run python -c "
   from schemas import ScreeningOut, RuleHit
   out = ScreeningOut(card_ref='CH0023', composite_score=0.933, flagged=True, decision='decline',
                      hits=[RuleHit(rule_name='AmountDeviationRule', score=1.0, reason='26.89x baseline'),
                            RuleHit(rule_name='UnusualHourRule', score=0.8, reason='02:00')])
   print(out.model_dump_json(indent=2))
   "
   ```

7. Load real database rows THROUGH the model to catch any dirty data

   ```bash
   uv run python -c "
   import sqlite3
   from pydantic import ValidationError
   from schemas import TransactionIn
   con = sqlite3.connect('cardguard.db')
   con.row_factory = sqlite3.Row
   ok = bad = 0
   for r in con.execute('SELECT * FROM transactions LIMIT 500'):
       try:
           TransactionIn(**{k: r[k] for k in ('card_ref','ts','amount','merchant_category','city','lat','lon')})
           ok += 1
       except ValidationError:
           bad += 1
   print(f'validated {ok}, rejected {bad}')
   "
   ```

8. Note the trade: hand-written validation is explicit but verbose; Pydantic is declarative and reports all errors at once.

## Verify

Valid input constructs and normalises; invalid input reports every field error; ScreeningOut serialises to JSON; 500 real rows validate cleanly.
