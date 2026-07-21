# Rewrite the prompt using the four-part pattern — goal, constraints, inputs, expected output
Ask the assistant: Write a Python function score_transaction(amount: float, is_overseas: bool, hour: int) -> dict that returns a risk score from 0 to 100 and the reasons that contributed to it. Add 40 points when the amount exceeds $500, 30 points when the merchant is overseas, and 20 points when the hour is between 1am and 5am. Cap the score at 100. Raise ValueError for a negative amount or an hour outside 0-23. Return the score and a list of reason strings.

