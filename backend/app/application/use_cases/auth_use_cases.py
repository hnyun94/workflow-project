from typing import Optional
from .base import UseCase, UseCaseRequest, UseCaseResponse, SuccessResponse, ErrorResponse
from ..dto.auth_dto import LoginDto, UserDto, TokenDto
from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ...domain.services.auth_service import AuthenticationService

class LoginRequest(UseCaseRequest):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class RegisterRequest(UseCaseRequest):
    def __init__(self, email: str, username: str, password: str, department: str, role: str):
        self.email = email
        self.username = username
        self.password = password
        self.department = department
        self.role = role

class LoginUseCase(UseCase):
    """로그인 유스케이스"""
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthenticationService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def execute(self, request: LoginRequest) -> UseCaseResponse:
        try:
            user = self.auth_service.authenticate_user(request.email, request.password)
            if not user:
                return ErrorResponse("Invalid credentials", "Email or password is incorrect")
            
            if not user.is_active:
                return ErrorResponse("User inactive", "User account is deactivated")
            
            token = self.auth_service.generate_token(user)
            
            return SuccessResponse(
                TokenDto(
                    access_token=token,
                    token_type="bearer",
                    user=UserDto.from_entity(user)
                ),
                "Login successful"
            )
            
        except Exception as e:
            return ErrorResponse(str(e), "Login failed")

class RegisterUseCase(UseCase):
    """회원가입 유스케이스"""
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthenticationService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def execute(self, request: RegisterRequest) -> UseCaseResponse:
        try:
            # 이메일 중복 확인
            if self.user_repository.email_exists(request.email):
                return ErrorResponse("Email exists", "Email already registered")
            
            # 해시된 비밀번호 생성
            hashed_password = self.auth_service.hash_password(request.password)
            
            # 사용자 생성
            user = User(
                email=request.email,
                username=request.username,
                department=request.department,
                role=self._parse_role(request.role)
            )
            
            # 리포지토리로 전달하기 전에 해시된 비밀번호 설정
            user._hashed_password = hashed_password
            
            created_user = self.user_repository.create(user)
            
            return SuccessResponse(
                UserDto.from_entity(created_user),
                "Registration successful"
            )
            
        except Exception as e:
            return ErrorResponse(str(e), "Registration failed")
    
    def _parse_role(self, role_str: str):
        from ...domain.enums.common import UserRole
        role_map = {
            "admin": UserRole.ADMIN,
            "manager": UserRole.MANAGER,
            "user": UserRole.USER
        }
        return role_map.get(role_str.lower(), UserRole.USER)

class GetCurrentUserUseCase(UseCase):
    """현재 사용자 조회 유스케이스"""
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthenticationService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def execute(self, token: str) -> UseCaseResponse:
        try:
            email = self.auth_service.verify_token(token)
            if not email:
                return ErrorResponse("Invalid token", "Token verification failed")
            
            user = self.user_repository.get_by_email(email)
            if not user:
                return ErrorResponse("User not found", "User not found")
            
            if not user.is_active:
                return ErrorResponse("User inactive", "User account is deactivated")
            
            return SuccessResponse(
                UserDto.from_entity(user),
                "User retrieved successfully"
            )
            
        except Exception as e:
            return ErrorResponse(str(e), "Failed to get current user")
