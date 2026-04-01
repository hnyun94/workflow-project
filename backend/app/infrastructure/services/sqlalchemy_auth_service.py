from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ...domain.services.auth_service import AuthenticationService
from ...domain.entities.user import User
from ...infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from ...core.config_sqlite import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SQLAlchemyAuthService(AuthenticationService):
    """SQLAlchemy 인증 서비스 구현"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = SQLAlchemyUserRepository(db)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        
        # 모델에서 해시된 비밀번호 가져오기
        from ...models.user import User as UserModel
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user_model:
            return None
        
        if not self.verify_password(password, user_model.hashed_password):
            return None
        
        return user
    
    def generate_token(self, user: User) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return access_token
    
    def verify_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except JWTError:
            return None
    
    def hash_password(self, password: str) -> str:
        # 비밀번호 길이 제한 (72바이트)
        if len(password.encode('utf-8')) > 72:
            password = password[:72]
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        if not hashed_password:
            return False
        
        # 비밀번호 길이 제한 (72바이트)
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = plain_password[:72]
        return pwd_context.verify(plain_password, hashed_password)
    
    def is_token_expired(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            exp = payload.get("exp")
            if exp is None:
                return True
            
            return datetime.utcnow().timestamp() > exp
        except JWTError:
            return True
    
    def refresh_token(self, token: str) -> Optional[str]:
        email = self.verify_token(token)
        if not email:
            return None
        
        user = self.user_repository.get_by_email(email)
        if not user or not user.is_active:
            return None
        
        return self.generate_token(user)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
