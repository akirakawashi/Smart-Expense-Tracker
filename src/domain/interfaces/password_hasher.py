from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    """Interface for password hashing."""
    
    @abstractmethod
    async def hash(self, password: str) -> str:
        """Hash a plain text password."""
        pass
    
    @abstractmethod
    async def verify(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        pass