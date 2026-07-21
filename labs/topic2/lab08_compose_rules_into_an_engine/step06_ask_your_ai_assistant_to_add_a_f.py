# Ask your AI assistant to add a fifth rule and confirm the engine needs no edit
Ask the assistant: Add a RoundAmountRule to rules.py that subclasses FraudRule with weight 0.4 and returns score 0.5 when the transaction amount is an exact multiple of 100, since round-number testing charges are a common card-testing signal. Do not modify RuleEngine.

