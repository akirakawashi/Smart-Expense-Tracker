"""
INFRASTRUCTURE — ORM models (SQLModel)
=======================================
These classes describe HOW domain entities are stored in PostgreSQL.

Key principle: ORM models and domain entities are SEPARATE classes.

Domain entity User  (domain/entities/user.py):
  - Plain Python dataclass
  - Contains business logic
  - No SQLModel / SQLAlchemy dependency

ORM model UserModel (this file):
  - SQLModel table
  - Knows about columns, indexes, FK constraints
  - No business logic

The repository layer translates between the two (ORM ↔ Domain).
"""

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class UserModel(SQLModel, table=True):
    """
    Maps to the 'users' table.

    user_id — auto-increment primary key assigned by PostgreSQL.
    The application never sets this value; it arrives after INSERT.
    """

    __tablename__ = "users"

    user_id: int | None = Field(
        default=None,
        primary_key=True,
        description="Auto-increment primary key",
    )
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    username: str = Field(max_length=50, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    telegram_chat_id: int | None = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # One user → many transactions
    transactions: list["TransactionModel"] = Relationship(back_populates="user")


class TransactionModel(SQLModel, table=True):
    """
    Maps to the 'transactions' table.

    transaction_id — auto-increment primary key assigned by PostgreSQL.
    user_id        — foreign key referencing users.user_id (CASCADE DELETE).
    """

    __tablename__ = "transactions"

    transaction_id: int | None = Field(
        default=None,
        primary_key=True,
        description="Auto-increment primary key",
    )
    user_id: int = Field(
        foreign_key="users.user_id",
        nullable=False,
        index=True,
        description="FK → users.user_id",
    )
    amount: float = Field(nullable=False, description="Transaction amount, always > 0")
    type: str = Field(max_length=10, nullable=False, description="'income' or 'expense'")
    category: str = Field(max_length=30, nullable=False)
    description: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Many transactions → one user
    user: UserModel | None = Relationship(back_populates="transactions")
