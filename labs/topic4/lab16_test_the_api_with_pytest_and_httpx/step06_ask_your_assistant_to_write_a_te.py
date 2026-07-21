# Ask your assistant to write a test for a gap — then verify it FAILS first
Ask the assistant: Write a pytest test asserting that POST /screen with amount exactly 1000000 succeeds but 1000001 returns 422, matching the Field(le=1_000_000) constraint in TransactionIn.

