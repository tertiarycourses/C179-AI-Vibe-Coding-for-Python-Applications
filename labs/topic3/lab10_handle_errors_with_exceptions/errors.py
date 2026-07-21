# errors.py
class CardGuardError(Exception):
    """Base class for every CardGuard failure — callers can catch this one type."""

class DataSourceError(CardGuardError):
    """The transaction store could not be read."""

class ValidationError(CardGuardError):
    """A transaction failed validation before scoring."""
    def __init__(self, field: str, value, message: str):
        self.field, self.value = field, value
        super().__init__(f"{field}={value!r}: {message}")

class RuleExecutionError(CardGuardError):
    """A scoring rule raised while screening a transaction."""

