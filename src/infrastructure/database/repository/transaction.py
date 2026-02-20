from src.domain.interfaces.transaction_repo import ITransactionRepository
from infrastructure.database.models.transaction import TransactionModel
from sqlalchemy.ext.asyncio import AsyncSession

class TransactionRepository(ITransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_entity():
        pass
        
    def _to_model():
        pass