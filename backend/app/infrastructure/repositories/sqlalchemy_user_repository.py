from typing import List, Optional
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User
from ...domain.enums.common import UserRole
from ...models.user import User as UserModel

class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy 사용자 리포지토리 구현"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        models = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    def create(self, entity: User) -> User:
        model = self._entity_to_model(entity)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, entity: User) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == entity.id).first()
        if not model:
            return None
        
        model.email = entity.email
        model.username = entity.username
        model.department = entity.department
        model.role = entity.role.value
        model.is_active = entity.is_active
        
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def delete(self, id: int) -> bool:
        model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
    
    def exists(self, id: int) -> bool:
        return self.db.query(UserModel).filter(UserModel.id == id).first() is not None
    
    def get_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def get_by_role(self, role: UserRole) -> List[User]:
        models = self.db.query(UserModel).filter(UserModel.role == role.value).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_active_users(self) -> List[User]:
        models = self.db.query(UserModel).filter(UserModel.is_active == True).all()
        return [self._model_to_entity(model) for model in models]
    
    def email_exists(self, email: str) -> bool:
        return self.db.query(UserModel).filter(UserModel.email == email).first() is not None
    
    def update_last_login(self, user_id: int) -> bool:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not model:
            return False
        
        # TODO: last_login 필드 추가 필요
        self.db.commit()
        return True
    
    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            department=model.department,
            role=UserRole(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            hashed_password=getattr(entity, '_hashed_password', ''),
            department=entity.department,
            role=entity.role.value,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
