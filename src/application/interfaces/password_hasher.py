from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    """Contract for password hashing. Decouples the algorithm from business logic."""

    @abstractmethod
    async def hash(self, plain_password: str) -> str:
        """Hash a plain-text password and return the hash string."""
        ...

    @abstractmethod
    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Return True if plain_password matches the stored hash."""
        ...
