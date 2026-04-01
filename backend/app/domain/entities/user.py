from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..enums import UserRole

@dataclass
class User:
    """사용자 도메인 엔티티"""
    id: Optional[int] = None
    email: str = ""
    username: str = ""
    department: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """도메인 규칙 검증"""
        if not self.email:
            raise ValueError("Email is required")
        if not self.username:
            raise ValueError("Username is required")
        if "@" not in self.email:
            raise ValueError("Invalid email format")
    
    def can_manage_supplies(self) -> bool:
        """비품 관리 권한 확인"""
        return self.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    def can_approve_reservations(self) -> bool:
        """예약 승인 권한 확인"""
        return self.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    def is_admin(self) -> bool:
        """관리자 확인"""
        return self.role == UserRole.ADMIN
    
    def activate(self):
        """사용자 활성화"""
        self.is_active = True
    
    def deactivate(self):
        """사용자 비활성화"""
        self.is_active = False
