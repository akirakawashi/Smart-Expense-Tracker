from abc import ABC, abstractmethod

from src.domain.entities.user import User


class IUserRepository(ABC):
    """
    Contract for the user repository.

    The Application layer depends on this interface, not on a concrete class.
    Benefits:
    - PostgreSQL can be swapped for MongoDB in tests via a mock repository.
    - The ORM can be replaced without touching any business logic.
    """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """Fetch a user by their ID."""
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by their email address."""
        ...

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Persist a new user and return the saved entity.
        The returned entity will have id populated by the database.
        """
        ...

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user and return the updated entity."""
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Delete a user by their ID."""
        ...
