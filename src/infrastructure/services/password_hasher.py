from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from src.application.interfaces.password_hasher import IPasswordHasher


class Argon2PasswordHasher(IPasswordHasher):
    """
    Implements IPasswordHasher using argon2-cffi (Argon2id).

    Argon2id won the Password Hashing Competition (2015) and is resistant
    to GPU and ASIC brute-force attacks, unlike bcrypt.

    Default parameters (argon2-cffi):
      time_cost=3, memory_cost=65536 (64 MB), parallelism=4
    """

    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    async def hash(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return self._hasher.verify(hashed_password, plain_password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False
