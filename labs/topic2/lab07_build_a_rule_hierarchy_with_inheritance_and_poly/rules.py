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

