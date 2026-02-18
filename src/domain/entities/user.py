from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """
    Domain Entity: User.
    """
    user_id: Optional[int] = None  # DB auto-increment id
    email: str
    username: str
    hashed_password: str
    number: Optional[str] = None
    balance: float = 0.0
    date_created: datetime = field(default_factory=datetime.now)

    def deposit(self, amount: float) -> None:
        """Deposit amount to the user's balance."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw amount from the user's balance."""
        if amount > self.balance:
            raise ValueError("Not enough balance for withdrawal")
        self.balance -= amount