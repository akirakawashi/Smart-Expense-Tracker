from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from sqlalchemy import Column, DateTime, Enum as SQLEnum
from infrastructure.database.base import Base
from src.domain.entities.transaction import TransactionType, TransactionCategory

if TYPE_CHECKING:
    from infrastructure.database.models.users import UserModel

class TransactionModel(Base, table=True):
    """
    SQLModel for transactions table.
    Maps to Domain Entity: Transaction
    """

    __tablename__ = "transactions"

    transaction_id: Optional[int] = Field(
        default=None, 
        primary_key=True, 
        description="Transaction ID"
    )
    
    user_id: int = Field(
        foreign_key="users.user_id", 
        ondelete="CASCADE", 
        index=True, 
        nullable=False,
        description="User ID who owns this transaction"
    )
    
    transaction_type: TransactionType = Field(
        sa_column=Column(
            SQLEnum(TransactionType, name="transaction_type"), 
            nullable=False
        ),
        description="Income or Expense"
    )
    
    amount: float = Field(
        nullable=False, 
        description="Transaction amount"
    )
    
    category: TransactionCategory = Field(
        sa_column=Column(
            SQLEnum(TransactionCategory, name="transaction_category"), 
            nullable=False
        ),
        description="Transaction category"
    )
    
    date_created: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime, default=datetime.now, nullable=False, index=True),
        description="Date transaction was created"
    )

    user: Optional["UserModel"] = Relationship(
        back_populates="transactions"
    )