from dataclasses import dataclass
from src.domain.entities.user import User
from src.domain.entities.transaction import Transaction, TransactionCategory, TransactionType
from src.domain.interfaces.user_repo import IUserRepository
from src.domain.interfaces.transaction_repo import ITransactionRepository
from src.application.dto.user_response import UserResponseDTO

@dataclass
class DepositRequest:
    user_id: int
    amount: float
    transaction_type: TransactionType = TransactionType.INCOME
    category: TransactionCategory = TransactionCategory.OTHER

class DepositUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        transaction_repo: ITransactionRepository,
    ):
        self.user_repo = user_repo
        self.transaction_repo = transaction_repo

    async def execute(self, request: DepositRequest) -> UserResponseDTO:

        if request.amount <= 0:
            raise ValueError("Amount must be positive")

        current_user = await self.user_repo.get_by_id(request.user_id)
        if not current_user:
            raise ValueError("User not found")
        
        current_user.deposit(request.amount) 

        await self.user_repo.update(current_user)
        
        new_transaction = Transaction(
            user_id=current_user.user_id,
            transaction_type=request.transaction_type,
            amount=request.amount,
            category=request.category,  
        )

        await self.transaction_repo.create(new_transaction)

        return UserResponseDTO(
            user_id=current_user.user_id,
            email=current_user.email,
            username=current_user.username,
            number=current_user.number,   
            balance=current_user.balance,
            date_created=current_user.date_created, 
        )
