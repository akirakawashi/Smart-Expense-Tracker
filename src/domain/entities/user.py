from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """
    Domain entity: User.

    id is int | None:
    - None  — the entity has not been persisted yet (before INSERT)
    - int   — assigned by the database after INSERT (auto-increment)

    The application never generates the ID itself.
    """

    id: int | None  # None before DB insert, set by DB after
    email: str
    username: str
    hashed_password: str
    is_active: bool
    telegram_chat_id: int | None
    created_at: datetime
    updated_at: datetime

    def is_telegram_linked(self) -> bool:
        """Return True if a Telegram account is linked to this user."""
        return self.telegram_chat_id is not None

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
