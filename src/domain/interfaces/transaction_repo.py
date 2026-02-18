from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from src.domain.entities.transaction import Transaction, TransactionCategory, TransactionType

class ITransactionRepository(ABC):
    """interface for transaction repository."""

    @abstractmethod
    async def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get a transaction by its ID."""
        pass

    @abstractmethod
    async def get_by_user_id(
        self, 
        user_id: int, 
        transaction_type: Optional[TransactionType] = None,
        category: Optional[TransactionCategory] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        limit: Optional[int] = None,
        offset: int = 0,
        ) -> List[Transaction]:
        """
        Get transactions for a user with filters.
        Filters map directly to SQL WHERE clauses for performance.
        """    
        pass
    
    @abstractmethod
    async def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction and return the created entity with id."""
        pass
    
    @abstractmethod
    async def get_total_by_user(
        self, 
        user_id: int, 
        transaction_type: Optional[TransactionType] = None
    ) -> float:
        """Get sum of transactions (for balance verification)."""
        pass