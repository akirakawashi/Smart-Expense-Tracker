from src.domain.interfaces.transaction_repo import ITransactionRepository
from src.domain.interfaces.transaction_repo import Transaction
from infrastructure.database.models.transaction import TransactionModel
from sqlalchemy.ext.asyncio import AsyncSession

class TransactionRepository(ITransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_entity(self, model: TransactionModel) -> Transaction:
        """
        Convert ORM model to Domain entity.
        """
        return Transaction(
            transaction_id=model.transaction_id,
            user_id=model.user_id,
            transaction_type=model.transaction_type,
            amount=model.amount,
            category=model.category,
            date_created=model.date_created,
        )
        
    def _to_model(self, entity: Transaction) -> TransactionModel:
        """
        Convert Domain entity to ORM model.
        """
        return TransactionModel(
            transaction_id=entity.transaction_id,
            user_id=entity.user_id,
            transaction_type=entity.transaction_type,
            amount=entity.amount,
            category=entity.category,
            date_created=entity.date_created,
        )