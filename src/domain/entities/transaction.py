from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    OTHER = "other"

@dataclass
class Transaction:
    """
    Domain Entity: Transaction.
    """
    transaction_id: Optional[int] = None
    user_id: int
    transaction_type: TransactionType
    amount: float
    category: TransactionCategory
    date_created: datetime = field(default_factory=datetime.now)