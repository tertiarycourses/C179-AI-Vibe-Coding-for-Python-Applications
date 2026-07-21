# Add the engine itself
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

