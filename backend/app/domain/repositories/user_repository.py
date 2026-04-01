from typing import List, Optional
from .base import Repository
from ..entities.user import User
from ..enums.common import UserRole

class UserRepository(Repository[User]):
    """사용자 리포지토리 인터페이스"""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        pass
    
    @abstractmethod
    def get_by_role(self, role: UserRole) -> List[User]:
        """역할별 사용자 조회"""
        pass
    
    @abstractmethod
    def get_active_users(self) -> List[User]:
        """활성 사용자 조회"""
        pass
    
    @abstractmethod
    def email_exists(self, email: str) -> bool:
        """이메일 중복 확인"""
        pass
    
    @abstractmethod
    def update_last_login(self, user_id: int) -> bool:
        """마지막 로그인 시간 업데이트"""
        pass
