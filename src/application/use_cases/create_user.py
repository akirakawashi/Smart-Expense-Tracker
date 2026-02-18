from dataclasses import dataclass
from typing import Optional
from src.domain.entities.user import User
from src.domain.interfaces.user_repo import IUserRepository
from src.domain.interfaces.password_hasher import IPasswordHasher
from src.application.dto.user_response import UserResponse 

@dataclass
class CreateUserRequest:
    """DTO for creating a new user."""
    email: str
    username: str
    password: str
    number: Optional[str] = None

class CreateUserUseCase:
    def __init__(
            self, 
            user_repo: IUserRepository, 
            password_hasher: IPasswordHasher
        ): # -> None??
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def execute(self, request: CreateUserRequest) -> UserResponse:
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            raise ValueError(f"Email {request.email} is already registered")
        
        hashed_password = await self.password_hasher.hash(request.password)

        new_user = User(
            email=request.email,
            username=request.username,
            hashed_password=hashed_password,
            number=request.number,
            balance=0.0,
        )

        created_user = await self.user_repo.create(new_user)

        return UserResponse(
            user_id=created_user.user_id,  # type: ignore[arg-type]
            email=created_user.email,
            username=created_user.username,
            number=created_user.number,
            balance=created_user.balance,
            date_created=created_user.date_created,
        )