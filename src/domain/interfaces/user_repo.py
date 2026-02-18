from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User

class IUserRepository(ABC):
    """interface for user repository."""

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user and return the created entity with id."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user and return the updated entity."""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Delete a user by their ID."""
        pass