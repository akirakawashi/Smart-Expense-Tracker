from abc import ABC, abstractmethod

from src.domain.entities.transaction import TransactionCategory


class IAICategorizer(ABC):
    """Contract for AI-based transaction categorisation."""

    @abstractmethod
    async def categorize(self, description: str) -> TransactionCategory:
        """
        Determine the category of a transaction from its description.

        Example: "Uber ride to the airport" → TransactionCategory.TRANSPORT
        """
        ...
