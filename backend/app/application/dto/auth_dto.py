from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ...domain.entities.user import User

@dataclass
class UserDto:
    id: int
    email: str
    username: str
    department: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    @classmethod
    def from_entity(cls, user: User) -> 'UserDto':
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            department=user.department,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

@dataclass
class LoginDto:
    email: str
    password: str

@dataclass
class RegisterDto:
    email: str
    username: str
    password: str
    department: str
    role: str

@dataclass
class TokenDto:
    access_token: str
    token_type: str
    user: UserDto

@dataclass
class CreateUserDto:
    email: str
    username: str
    password: str
    department: Optional[str] = None
    role: str = "user"

@dataclass
class UpdateUserDto:
    username: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
