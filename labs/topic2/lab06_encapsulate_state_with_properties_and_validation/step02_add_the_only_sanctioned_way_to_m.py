# Add the only sanctioned way to move the baseline
    def observe(self, amount: float) -> None:
        """Fold one new transaction into the running baseline."""
        if amount < 0:
            raise ValueError("amount must not be negative")
        self._observed_count += 1
        weight = 1 / min(self._observed_count, 30)   # rolling, recency-weighted
        self._typical_amount = (1 - weight) * self._typical_amount + weight * amount

    def deviation_factor(self, amount: float) -> float:
        """How many times the baseline this amount represents."""
        return round(amount / self._typical_amount, 2)

