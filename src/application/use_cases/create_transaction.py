from datetime import datetime

from src.application.dto import CreateTransactionDTO, TransactionResponseDTO
from src.application.interfaces.ai_categorizer import IAICategorizer
from src.domain.entities.transaction import Transaction
from src.domain.interfaces.transaction_repository import ITransactionRepository
from src.domain.interfaces.user_repository import IUserRepository


class CreateTransactionUseCase:
    """
    Use case: create a new transaction.

    If no category is provided, the AI categoriser is called automatically.
    The AI service is injected as an abstraction — the use case doesn't know
    which model (GPT-4, mock, etc.) is being used.
    """

    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        user_repository: IUserRepository,
        ai_categorizer: IAICategorizer,
    ) -> None:
        self._transaction_repo = transaction_repository
        self._user_repo = user_repository
        self._ai_categorizer = ai_categorizer

    async def execute(self, user_id: int, dto: CreateTransactionDTO) -> TransactionResponseDTO:
        # Step 1: ensure the user exists
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User {user_id} not found")

        # Step 2: resolve category — manual or via AI
        if dto.category is not None:
            category = dto.category
        else:
            category = await self._ai_categorizer.categorize(dto.description)

        # Step 3: build domain entity
        # id=None because the DB will assign it on INSERT (auto-increment)
        now = datetime.utcnow()
        transaction = Transaction(
            id=None,
            user_id=user_id,
            amount=dto.amount,
            type=dto.type,
            category=category,
            description=dto.description,
            created_at=now,
            updated_at=now,
        )

        # Step 4: validate domain invariants
        transaction.validate()

        # Step 5: persist — repository returns entity with id set by DB
        saved = await self._transaction_repo.create(transaction)

        return TransactionResponseDTO(
            id=saved.id,
            user_id=saved.user_id,
            amount=saved.amount,
            type=saved.type,
            category=saved.category,
            description=saved.description,
            created_at=saved.created_at,
        )


class UserNotFoundError(Exception):
    """Raised when the referenced user does not exist."""
    pass
