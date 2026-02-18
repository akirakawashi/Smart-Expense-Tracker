from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.entities.transaction import Transaction, TransactionCategory, TransactionType


class ITransactionRepository(ABC):
    """Contract for the transaction repository."""

    @abstractmethod
    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        """Fetch a single transaction by its ID."""
        ...

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: int,
        *,
        type: TransactionType | None = None,
        category: TransactionCategory | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Transaction]:
        """
        Fetch transactions for a user with optional filters.

        All filter parameters are keyword-only to avoid positional mistakes.
        When a filter is None it is ignored, returning all matching records.
        """
        ...

    @abstractmethod
    async def create(self, transaction: Transaction) -> Transaction:
        """
        Persist a new transaction and return the saved entity.
        The returned entity will have id populated by the database.
        """
        ...

    @abstractmethod
    async def delete(self, transaction_id: int) -> None:
        """Delete a transaction by its ID."""
        ...

    @abstractmethod
    async def get_summary(
        self,
        user_id: int,
        date_from: datetime,
        date_to: datetime,
    ) -> dict[str, float]:
        """
        Return aggregated totals per category for a given period.

        Returns: {category_value: total_amount}
        Example: {"food": 15400.0, "transport": 3200.0}
        """
        ...
