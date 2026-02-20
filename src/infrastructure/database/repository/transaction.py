from typing import Optional, List
from sqlalchemy import func, case
from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.transaction import Transaction
from src.domain.interfaces.transaction_repo import ITransactionRepository
from src.domain.entities.transaction import TransactionType, TransactionCategory
from infrastructure.database.models.transaction import TransactionModel

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
    
    async def get_by_id(
            self,
            transaction_id: int, 
        ) -> Optional[Transaction]:
        """
        
        """

        query = select(TransactionModel).where(TransactionModel.transaction_id == transaction_id)

        result = await self.session.execute(query)
        model = result.scalar_one_or_none

        return self._to_entity(model) if model else None
    
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
        """Get transactions for a user with filters."""
        
        query = select(TransactionModel).where(TransactionModel.user_id == user_id)
        
        if transaction_type:
            query = query.where(TransactionModel.transaction_type == transaction_type)
        
        if category:
            query = query.where(TransactionModel.category == category)
        
        if date_from:
            query = query.where(TransactionModel.date_created >= date_from)
        
        if date_to:
            query = query.where(TransactionModel.date_created <= date_to)
        
        if limit:
            query = query.limit(limit).offset(offset)
        
        query = query.order_by(TransactionModel.date_created.desc())
        
        result = await self.session.execute(query)
        
        models = result.scalars().all()
        transactions = [self._to_entity(model) for model in models]
        
        return transactions
    
    async def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        model = self._to_model(transaction)
        
        self.session.add(model)
        await self.session.flush() 
        
        transaction.transaction_id = model.transaction_id
        return transaction
        
    async def get_total_by_user(
        self, 
        user_id: int, 
        transaction_type: Optional[TransactionType] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> float:
        """
        Get sum of transactions (always positive).
        For statistics: "You spent 500 on food"
        """
        from sqlalchemy import func
        
        query = select(func.sum(TransactionModel.amount)).where(
            TransactionModel.user_id == user_id
        )
        
        if transaction_type:
            query = query.where(TransactionModel.transaction_type == transaction_type)
        
        if date_from:
            query = query.where(TransactionModel.date_created >= date_from)
        
        if date_to:
            query = query.where(TransactionModel.date_created <= date_to)
        
        result = await self.session.execute(query)
        total = result.scalar_one_or_none()
        
        return float(total) if total else 0.0