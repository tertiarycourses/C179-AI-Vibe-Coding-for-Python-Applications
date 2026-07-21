# Implement the velocity rule — it needs history, which the shared interface already provides
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

