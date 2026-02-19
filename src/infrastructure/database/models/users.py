from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from sqlalchemy import Column, DateTime
from infrastructure.database.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.transaction import TransactionModel

class UserModel(Base, table=True):
    """
    SQLModel for users table.
    Maps to Domain Entity: User
    """

    __tablename__ = "users"

    user_id: Optional[int] = Field(
        default=None, 
        primary_key=True, 
        description="User ID"
        )
    
    email: str = Field(
        unique=True, 
        nullable=False, 
        description="User email"
        )
    
    username: str = Field(
        nullable=False, 
        unique=False, 
        description="Username"
        )
    
    password: str = Field(
        nullable=False, 
        description="Hashed password"
        )
    
    number: Optional[str] = Field(
        default=None, 
        description="Phone number"
        )
    
    balance: float = Field(
        default=0.0, 
        description="User balance"
        )
    
    date_created: datetime = Field(
        default_factory=datetime.now, 
        sa_column=Column(DateTime, default=datetime.now), 
        description="Date created"
        )

    transactions: list["TransactionModel"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )