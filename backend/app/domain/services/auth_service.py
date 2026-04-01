from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User

class AuthenticationService(ABC):
    """인증 도메인 서비스"""
    
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """사용자 인증"""
        pass
    
    @abstractmethod
    def generate_token(self, user: User) -> str:
        """JWT 토큰 생성"""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[str]:
        """토큰 검증"""
        pass
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """비밀번호 해싱"""
        pass
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        pass
    
    @abstractmethod
    def is_token_expired(self, token: str) -> bool:
        """토큰 만료 확인"""
        pass
    
    @abstractmethod
    def refresh_token(self, token: str) -> Optional[str]:
        """토큰 갱신"""
        pass
