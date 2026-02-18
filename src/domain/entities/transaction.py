from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    """Transaction type — a business concept, not a raw DB string."""

    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(str, Enum):
    """
    Transaction categories.

    Defined in the domain — both the AI layer and Infrastructure
    use these same values.
    """

    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTH = "health"
    SALARY = "salary"
    FREELANCE = "freelance"
    OTHER = "other"


@dataclass
class Transaction:
    """
    Domain entity: Transaction.

    id is int | None:
    - None  — the entity has not been persisted yet (before INSERT)
    - int   — assigned by the database after INSERT (auto-increment)
    """

    id: int | None  # None before DB insert, set by DB after
    user_id: int
    amount: float
    type: TransactionType
    category: TransactionCategory
    description: str
    created_at: datetime
    updated_at: datetime

    def is_expense(self) -> bool:
        return self.type == TransactionType.EXPENSE

    def is_income(self) -> bool:
        return self.type == TransactionType.INCOME

    def validate(self) -> None:
        """
        Assert domain invariants.

        Rules:
        - amount must always be > 0
        - description must not be blank
        """
        if self.amount <= 0:
            raise ValueError(f"Transaction amount must be positive, got {self.amount}")
        if not self.description.strip():
            raise ValueError("Transaction description cannot be empty")
