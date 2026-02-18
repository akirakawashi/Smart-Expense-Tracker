from datetime import datetime

from src.application.dto import RegisterUserDTO, UserResponseDTO
from src.application.interfaces.password_hasher import IPasswordHasher
from src.domain.entities.user import User
from src.domain.interfaces.user_repository import IUserRepository


class RegisterUserUseCase:
    """
    Use case: register a new user.

    Steps:
    1. Ensure the email is not already taken (business rule).
    2. Hash the password.
    3. Build the User domain entity (id=None — not persisted yet).
    4. Persist via the repository — DB assigns the auto-increment id.
    5. Return a DTO (no password exposed).
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
    ) -> None:
        self._user_repo = user_repository
        self._password_hasher = password_hasher

    async def execute(self, dto: RegisterUserDTO) -> UserResponseDTO:
        # Step 1: email must be unique
        existing_user = await self._user_repo.get_by_email(dto.email)
        if existing_user is not None:
            raise EmailAlreadyExistsError(f"Email '{dto.email}' is already registered")

        # Step 2: hash the password via the abstraction
        hashed_password = await self._password_hasher.hash(dto.password)

        # Step 3: build the domain entity
        # id=None because the DB will assign it on INSERT (auto-increment)
        now = datetime.utcnow()
        user = User(
            id=None,
            email=dto.email,
            username=dto.username,
            hashed_password=hashed_password,
            is_active=True,
            telegram_chat_id=None,
            created_at=now,
            updated_at=now,
        )

        # Step 4: persist — repository returns the entity with id set by DB
        created_user = await self._user_repo.create(user)

        # Step 5: map to DTO — never expose the domain entity directly
        return UserResponseDTO(
            id=created_user.id,
            email=created_user.email,
            username=created_user.username,
            is_active=created_user.is_active,
            telegram_linked=created_user.is_telegram_linked(),
            created_at=created_user.created_at,
        )


class EmailAlreadyExistsError(Exception):
    """Raised by the Application layer when an email is already registered."""
    pass
