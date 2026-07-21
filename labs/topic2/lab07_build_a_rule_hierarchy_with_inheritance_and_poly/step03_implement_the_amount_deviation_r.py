# Implement the amount-deviation rule
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

