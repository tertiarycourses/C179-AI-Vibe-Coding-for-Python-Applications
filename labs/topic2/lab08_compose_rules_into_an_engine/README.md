# Lab 8 — Compose Rules into an Engine

**Topic 2** · Use composition to assemble behaviour from independent parts

The learner builds a RuleEngine that HAS-A list of rules rather than inheriting from any of them, producing a weighted composite score with a full explanation of every contributing rule.

- **You will build:** A RuleEngine returning a ScreeningResult with a composite score and per-rule reasons
- **Tools:** uv, Python 3.12

## Steps

1. Write the engine — note it inherits from nothing; it composes

   ```python
   # engine.py
   from dataclasses import dataclass, field
   from models import Transaction
   from cardholder import Cardholder
   from rules import FraudRule, RuleResult
   
   @dataclass
   class ScreeningResult:
       """The engine's decision, with every reason that produced it."""
       txn_id: int
       card_ref: str
       composite_score: float
       flagged: bool
       results: list[RuleResult] = field(default_factory=list)
   
       def explain(self) -> str:
           head = (f"Transaction {self.txn_id} ({self.card_ref}): "
                   f"score {self.composite_score} "
                   f"{'FLAGGED' if self.flagged else 'clean'}")
           lines = [f"    - {r.rule_name} {r.score} :: {r.reason}"
                    for r in self.results if r.score > 0]
           return "\n".join([head, *lines])
   ```

2. Add the engine itself

   ```python
   class RuleEngine:
       """Composes independent rules into one weighted decision."""
   
       def __init__(self, rules: list[FraudRule], threshold: float = 0.55):
           if not rules:
               raise ValueError("at least one rule is required")
           self.rules = rules
           self.threshold = threshold
   
       def screen(self, txn: Transaction, holder: Cardholder,
                  history: list[Transaction]) -> ScreeningResult:
           results = [r.score(txn, holder, history) for r in self.rules]
           total_weight = sum(r.weight for r in self.rules)
           composite = sum(res.score * rule.weight
                           for res, rule in zip(results, self.rules)) / total_weight
           composite = round(composite, 3)
           return ScreeningResult(txn.id, txn.card_ref, composite,
                                  composite >= self.threshold, results)
   ```

3. Screen a known-fraud transaction and read the explanation

   ```bash
   uv run python -c "
   import sqlite3
   from models import Transaction
   from cardholder import Cardholder
   from rules import AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule, VelocityRule
   from engine import RuleEngine
   con = sqlite3.connect('cardguard.db')
   row = con.execute('SELECT * FROM transactions WHERE is_known_fraud=1 ORDER BY amount DESC LIMIT 1').fetchone()
   txn = Transaction.from_row(row)
   holder = Cardholder(*con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders WHERE card_ref=?',(txn.card_ref,)).fetchone())
   eng = RuleEngine([AmountDeviationRule(), UnusualHourRule(), HighRiskCategoryRule(), VelocityRule()])
   print(eng.screen(txn, holder, []).explain())
   "
   ```

4. Screen a normal transaction and confirm it stays clean

   ```bash
   uv run python -c "
   import sqlite3
   from models import Transaction
   from cardholder import Cardholder
   from rules import AmountDeviationRule, UnusualHourRule, HighRiskCategoryRule, VelocityRule
   from engine import RuleEngine
   con = sqlite3.connect('cardguard.db')
   row = con.execute("SELECT * FROM transactions WHERE is_known_fraud=0 AND merchant_category='grocery' LIMIT 1").fetchone()
   txn = Transaction.from_row(row)
   holder = Cardholder(*con.execute('SELECT card_ref,name,home_city,typical_amount FROM cardholders WHERE card_ref=?',(txn.card_ref,)).fetchone())
   eng = RuleEngine([AmountDeviationRule(), UnusualHourRule(), HighRiskCategoryRule(), VelocityRule()])
   print(eng.screen(txn, holder, []).explain())
   "
   ```

5. Reconfigure the engine WITHOUT touching any rule class — composition in action

   ```bash
   uv run python -c "
   from rules import AmountDeviationRule, HighRiskCategoryRule
   from engine import RuleEngine
   strict = RuleEngine([AmountDeviationRule(alert_factor=4.0), HighRiskCategoryRule()], threshold=0.35)
   print('rules:', [r.name for r in strict.rules], 'threshold:', strict.threshold)
   "
   ```

6. Ask your AI assistant to add a fifth rule and confirm the engine needs no edit

   ```python
   Ask the assistant: Add a RoundAmountRule to rules.py that subclasses FraudRule with weight 0.4 and returns score 0.5 when the transaction amount is an exact multiple of 100, since round-number testing charges are a common card-testing signal. Do not modify RuleEngine.
   ```

7. Note the design principle: inheritance shares WHAT rules are; composition decides WHICH rules run.

## Verify

The engine flags the known-fraud transaction with a readable explanation, leaves a grocery transaction clean, and can be reconfigured with different rules and thresholds without editing any rule class.
