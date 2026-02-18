from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserResponseDTO:
    """
    Data Transfer Object for user response.
    """
    user_id: int
    email: str
    username: str
    number: Optional[str] = None
    balance: float
    date_created: datetime