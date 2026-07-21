# Lab 7 — Build a Rule Hierarchy with Inheritance and Polymorphism

**Topic 2** · Share behaviour through a base class and override it per rule

The learner defines an abstract FraudRule base class and implements four concrete rules. Each rule scores a transaction differently but presents an identical interface, so the caller never needs to know which rule it holds.

- **You will build:** An abstract FraudRule plus AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule and VelocityRule
- **Tools:** uv, Python 3.12, abc

## Steps

1. Define the contract every rule must satisfy

   ```python
   # rules.py
   from abc import ABC, abstractmethod
   from dataclasses import dataclass
   from models import Transaction
   from cardholder import Cardholder
   
   @dataclass
   class RuleResult:
       """One rule's verdict on one transaction."""
       rule_name: str
       score: float          # 0.0 (clean) .. 1.0 (certain)
       reason: str
   
   class FraudRule(ABC):
       """Base class: every rule scores a transaction from 0.0 to 1.0."""
   
       weight: float = 1.0
   
       @property
       def name(self) -> str:
           return self.__class__.__name__
   
       @abstractmethod
       def score(self, txn: Transaction, holder: Cardholder,
                 history: list[Transaction]) -> RuleResult:
           """Return this rule's verdict. Must be implemented by every subclass."""
   ```

2. Prove the abstract class cannot be instantiated — the contract is enforced

   ```bash
   uv run python -c "
   from rules import FraudRule
   try:
       FraudRule()
   except TypeError as e:
       print('correctly blocked:', e)
   "
   ```

3. Implement the amount-deviation rule

   ```python
   class AmountDeviationRule(FraudRule):
       """Flags spend far above this cardholder's own baseline."""
       weight = 1.2
   
       def __init__(self, alert_factor: float = 8.0):
           self.alert_factor = alert_factor
   
       def score(self, txn, holder, history):
           factor = holder.deviation_factor(txn.amount)
           s = min(factor / self.alert_factor, 1.0) if factor > 1 else 0.0
           return RuleResult(self.name, round(s, 3),
                             f"${txn.amount:,.2f} is {factor}x the ${holder.typical_amount:,.2f} baseline")
   ```

4. Implement the unusual-hour and high-risk-category rules

   ```python
   class UnusualHourRule(FraudRule):
       """Flags activity outside the cardholder's normal waking window."""
       weight = 0.6
   
       def score(self, txn, holder, history):
           s = 0.8 if txn.hour in {0, 1, 2, 3, 4, 5} else 0.0
           return RuleResult(self.name, s, f"transaction at {txn.hour:02d}:00")
   
   class HighRiskCategoryRule(FraudRule):
       """Flags merchant categories with elevated chargeback rates."""
       weight = 0.8
   
       RISK = {"crypto_exchange": 0.9, "gift_cards": 0.8,
               "jewellery": 0.6, "online_gaming": 0.5}
   
       def score(self, txn, holder, history):
           s = self.RISK.get(txn.merchant_category, 0.0)
           return RuleResult(self.name, s, f"category {txn.merchant_category}")
   ```

5. Implement the velocity rule — it needs history, which the shared interface already provides

   ```python
   from datetime import timedelta
   
   class VelocityRule(FraudRule):
       """Flags many transactions inside a short window."""
       weight = 1.5
   
       def __init__(self, window_minutes: int = 10, threshold: int = 4):
           self.window = timedelta(minutes=window_minutes)
           self.threshold = threshold
   
       def score(self, txn, holder, history):
           recent = [h for h in history
                     if 0 <= (txn.ts - h.ts).total_seconds() <= self.window.total_seconds()]
           n = len(recent) + 1
           s = min((n - 1) / self.threshold, 1.0) if n > 1 else 0.0
           return RuleResult(self.name, round(s, 3),
                             f"{n} transactions in {self.window.seconds // 60} minutes")
   ```

6. Call every rule through the SAME interface — this is polymorphism doing real work

   ```bash
   uv run python -c "
   import sqlite3
   from models import Transaction
   from cardholder import Cardholder
   from rules import AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule, VelocityRule
   con = sqlite3.connect('cardguard.db')
   row = con.execute('SELECT * FROM transactions WHERE is_known_fraud=1 ORDER BY amount DESC LIMIT 1').fetchone()
   txn = Transaction.from_row(row)
   chr_ = con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders WHERE card_ref=?', (txn.card_ref,)).fetchone()
   holder = Cardholder(*chr_)
   rules = [AmountDeviationRule(), UnusualHourRule(), HighRiskCategoryRule(), VelocityRule()]
   print(txn)
   for r in rules:
       res = r.score(txn, holder, [])
       print(f'  {res.rule_name:<24} {res.score:>5}  {res.reason}')
   "
   ```

7. Note what inheritance bought: adding a fifth rule requires no change to any caller.

## Verify

FraudRule cannot be instantiated; all four rules implement score() and return a RuleResult; a known-fraud transaction produces non-zero scores from the relevant rules.
