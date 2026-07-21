# Ask your assistant to add a rule-level guard so one broken rule cannot stop a screen
Ask the assistant: In RuleEngine.screen, wrap each rule call in try/except so that if one rule raises, the engine records a RuleExecutionError message on the result and continues scoring with the remaining rules. Never use a bare except.

