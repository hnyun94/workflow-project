from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...application.use_cases.auth_use_cases import (
    LoginUseCase, RegisterUseCase, GetCurrentUserUseCase,
    LoginRequest, RegisterRequest
)
from ...infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from ...infrastructure.services.sqlalchemy_auth_service import SQLAlchemyAuthService
from ...core.config_sqlite import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# 의존성 주입 설정
def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)

def get_auth_service(db: Session = Depends(get_db)) -> SQLAlchemyAuthService:
    return SQLAlchemyAuthService(db)

def get_login_use_case(
    user_repo = Depends(get_user_repository),
    auth_service = Depends(get_auth_service)
) -> LoginUseCase:
    return LoginUseCase(user_repo, auth_service)

def get_register_use_case(
    user_repo = Depends(get_user_repository),
    auth_service = Depends(get_auth_service)
) -> RegisterUseCase:
    return RegisterUseCase(user_repo, auth_service)

def get_current_user_use_case(
    user_repo = Depends(get_user_repository),
    auth_service = Depends(get_auth_service)
) -> GetCurrentUserUseCase:
    return GetCurrentUserUseCase(user_repo, auth_service)

def get_current_user_dependency(
    token: str = Depends(oauth2_scheme),
    use_case: GetCurrentUserUseCase = Depends(get_current_user_use_case)
):
    """현재 사용자 가져오기 의존성"""
    response = use_case.execute(token)
    
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return response.data.user

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginUseCase = Depends(get_login_use_case)
):
    """로그인"""
    request = LoginRequest(email=form_data.username, password=form_data.password)
    response = use_case.execute(request)
    
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return response.data

@router.post("/register")
async def register(
    user_data: dict,
    use_case: RegisterUseCase = Depends(get_register_use_case)
):
    """회원가입"""
    request = RegisterRequest(**user_data)
    response = use_case.execute(request)
    
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.error
        )
    
    return response.data

@router.get("/me")
async def get_current_user_info(
    current_user = Depends(get_current_user_dependency)
):
    """현재 사용자 정보"""
    return current_user

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginUseCase = Depends(get_login_use_case)
):
    """액세스 토큰 발급 (OAuth2 호환)"""
    request = LoginRequest(email=form_data.username, password=form_data.password)
    response = use_case.execute(request)
    
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": response.data.access_token,
        "token_type": response.data.token_type
    }
