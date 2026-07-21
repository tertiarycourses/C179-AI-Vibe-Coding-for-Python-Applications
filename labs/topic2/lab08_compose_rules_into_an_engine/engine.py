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

