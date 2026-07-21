# Lab 2 — Write Effective Prompts for an AI Coding Assistant

**Topic 1** · Apply prompting patterns that produce correct, reviewable code

The learner contrasts a vague prompt with a specified prompt on the same task, then applies the goal-constraints-inputs-output pattern to generate a function that handles real edge cases.

- **You will build:** Two versions of a transaction risk-scoring function and a written comparison of the prompts that produced them
- **Tools:** AI coding assistant (Claude / Copilot / Cursor), uv, Python

## Steps

1. Start from the vague prompt and record exactly what you get back

   ```python
   Ask the assistant: write a function to score a transaction
   ```

2. Read the generated code critically — list what it assumed. Typical gaps: what counts as high value, whether an overseas merchant matters, what the score range is, what happens for a negative amount.
3. Rewrite the prompt using the four-part pattern — goal, constraints, inputs, expected output

   ```python
   Ask the assistant: Write a Python function score_transaction(amount: float, is_overseas: bool, hour: int) -> dict that returns a risk score from 0 to 100 and the reasons that contributed to it. Add 40 points when the amount exceeds $500, 30 points when the merchant is overseas, and 20 points when the hour is between 1am and 5am. Cap the score at 100. Raise ValueError for a negative amount or an hour outside 0-23. Return the score and a list of reason strings.
   ```

4. Save the improved result and read every line before running it

   ```python
   # scoring.py
   def score_transaction(amount: float, is_overseas: bool, hour: int) -> dict:
       """Return a 0-100 risk score for one transaction, with its reasons."""
       if amount < 0:
           raise ValueError("amount must not be negative")
       if not 0 <= hour <= 23:
           raise ValueError("hour must be between 0 and 23")
   
       HIGH_VALUE = 500.00
       score, reasons = 0, []
   
       if amount > HIGH_VALUE:
           score += 40
           reasons.append("high value")
       if is_overseas:
           score += 30
           reasons.append("overseas merchant")
       if 1 <= hour <= 5:
           score += 20
           reasons.append("unusual hour")
   
       return {"score": min(score, 100), "reasons": reasons}
   ```

5. Test the boundaries the prompt specified — this is where generated code usually fails

   ```bash
   uv run python -c "
   from scoring import score_transaction
   print(score_transaction(42.90, False, 14))   # low risk
   print(score_transaction(800.00, True, 3))    # every rule fires
   print(score_transaction(500.00, False, 14))  # exactly on the threshold
   "
   ```

6. Confirm the error paths actually raise

   ```bash
   uv run python -c "
   from scoring import score_transaction
   try:
       score_transaction(-100, False, 14)
   except ValueError as e:
       print('correctly raised:', e)
   "
   ```

7. Write two sentences in your notes: which prompt produced code you would ship, and why.

## Verify

The specified prompt produces a function that caps the score at 100, fires each rule independently, and raises ValueError on invalid input. The learner can state why the vague prompt was insufficient.
