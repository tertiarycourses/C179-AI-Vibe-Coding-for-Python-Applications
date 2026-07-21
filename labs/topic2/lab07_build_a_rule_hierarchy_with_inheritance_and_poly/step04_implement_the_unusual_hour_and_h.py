# Implement the unusual-hour and high-risk-category rules
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

