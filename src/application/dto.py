from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.domain.entities.transaction import TransactionCategory, TransactionType


# ---------------------------------------------------------------------------
# User DTOs
# ---------------------------------------------------------------------------

class RegisterUserDTO(BaseModel):
    """Payload for user registration. Received from the Presentation layer."""

    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UserResponseDTO(BaseModel):
    """Safe user response — password is never included."""

    id: int
    email: str
    username: str
    is_active: bool
    telegram_linked: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Transaction DTOs
# ---------------------------------------------------------------------------

class CreateTransactionDTO(BaseModel):
    """Payload for creating a transaction."""

    amount: float = Field(gt=0, description="Amount must be greater than 0")
    type: TransactionType
    category: TransactionCategory | None = None  # None → AI will determine
    description: str = Field(min_length=1, max_length=255)


class TransactionResponseDTO(BaseModel):
    """Transaction data returned to the client."""

    id: int
    user_id: int
    amount: float
    type: TransactionType
    category: TransactionCategory
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionFilterDTO(BaseModel):
    """Query filters for listing transactions."""

    type: TransactionType | None = None
    category: TransactionCategory | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
