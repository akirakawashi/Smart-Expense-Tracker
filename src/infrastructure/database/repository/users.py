from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from src.domain.interfaces.user_repo import IUserRepository
from infrastructure.database.models.users import UserModel

class UserRepository(IUserRepository):
    """
    Implementation of IUserRepository using SQLModel + PostgreSQL.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """Convert ORM model to Domain entity."""
        return User(
            user_id=model.user_id,
            email=model.email,
            username=model.username,
            hashed_password=model.password, 
            number=model.number,
            balance=model.balance,
            date_created=model.date_created,
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convert Domain entity to ORM model."""
        return UserModel(
            user_id=entity.user_id,
            email=entity.email,
            username=entity.username,
            password=entity.hashed_password,
            number=entity.number,
            balance=entity.balance,
            date_created=entity.date_created,
        )
    
    async def get_by_id(
            self,
            user_id: int,
            with_lock: bool = True,
        ) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User's primary key
            with_lock: If True, lock the row for update (prevents race conditions)
        """

        query = select(UserModel).where(UserModel.user_id == user_id)

        if with_lock:
            query = query.with_for_update()

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        return self._to_entity(model) if model else None
    
    async def get_by_email(
            self, 
            email: str
            ) -> Optional[User]:
        """Get user by email address."""

        query = select(UserModel).where(UserModel.email == email)
        
        result = await self.session.execute(query)
        model = result.scalar_one_or_none

        return self._to_entity(model) if model else None

    async def create(
            self, 
            user: User
            ) -> User:
        """
        Create a new user in database.
        Returns the created user with generated ID.
        """

        model = self._to_model(user)
        
        self.session.add(model)
        await self.session.flush() 
        
        user.user_id = model.user_id
        
        return user
    
    async def update(
            self,
            user: User,
            )->User:
        """
        Update an existing user.
        Returns the updated user.
        """
        model = self._to_model(user)

        updated_model = await self.session.merge(model)
        await self.session.flush()

        return self._to_entity(updated_model)

    async def delete(
        self, 
        user_id: int
        ) -> None:
        """Delete user by ID."""
        
        query = select(UserModel).where(UserModel.user_id == user_id)
        
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        
        if model:
            await self.session.delete(model)
