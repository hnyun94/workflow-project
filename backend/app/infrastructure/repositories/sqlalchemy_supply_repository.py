from typing import List, Optional
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from ...domain.repositories.supply_repository import SupplyRepository, SupplyCategoryRepository
from ...domain.entities.supply import Supply, SupplyCategory
from ...domain.enums.common import SupplyStatus
from ...models.supply import Supply as SupplyModel, SupplyCategory as SupplyCategoryModel

class SQLAlchemySupplyRepository(SupplyRepository):
    """SQLAlchemy 비품 리포지토리 구현"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[Supply]:
        model = self.db.query(SupplyModel).filter(SupplyModel.id == id).first()
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Supply]:
        models = self.db.query(SupplyModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    def create(self, entity: Supply) -> Supply:
        model = self._entity_to_model(entity)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, entity: Supply) -> Optional[Supply]:
        model = self.db.query(SupplyModel).filter(SupplyModel.id == entity.id).first()
        if not model:
            return None
        
        # 필드 업데이트
        model.name = entity.name
        model.description = entity.description
        model.category_id = entity.category_id
        model.quantity = entity.quantity
        model.min_quantity = entity.min_quantity
        model.unit = entity.unit
        model.location = entity.location
        model.status = entity.status.value
        model.price = entity.price
        
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def delete(self, id: int) -> bool:
        model = self.db.query(SupplyModel).filter(SupplyModel.id == id).first()
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
    
    def exists(self, id: int) -> bool:
        return self.db.query(SupplyModel).filter(SupplyModel.id == id).first() is not None
    
    def get_by_category(self, category_id: int) -> List[Supply]:
        models = self.db.query(SupplyModel).filter(SupplyModel.category_id == category_id).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_by_status(self, status: SupplyStatus) -> List[Supply]:
        models = self.db.query(SupplyModel).filter(SupplyModel.status == status.value).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_low_stock_supplies(self) -> List[Supply]:
        models = self.db.query(SupplyModel).filter(
            SupplyModel.quantity <= SupplyModel.min_quantity
        ).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_available_supplies(self) -> List[Supply]:
        models = self.db.query(SupplyModel).filter(
            SupplyModel.status == SupplyStatus.AVAILABLE.value,
            SupplyModel.quantity > 0
        ).all()
        return [self._model_to_entity(model) for model in models]
    
    def search_by_name(self, name: str) -> List[Supply]:
        models = self.db.query(SupplyModel).filter(
            SupplyModel.name.ilike(f"%{name}%")
        ).all()
        return [self._model_to_entity(model) for model in models]
    
    def update_quantity(self, supply_id: int, new_quantity: int) -> Optional[Supply]:
        model = self.db.query(SupplyModel).filter(SupplyModel.id == supply_id).first()
        if not model:
            return None
        
        model.quantity = new_quantity
        
        # 상태 자동 업데이트
        if new_quantity == 0:
            model.status = SupplyStatus.OUT_OF_STOCK.value
        elif new_quantity <= model.min_quantity:
            model.status = SupplyStatus.AVAILABLE.value
        else:
            model.status = SupplyStatus.AVAILABLE.value
        
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def _model_to_entity(self, model: SupplyModel) -> Supply:
        return Supply(
            id=model.id,
            name=model.name,
            description=model.description,
            category_id=model.category_id,
            quantity=model.quantity,
            min_quantity=model.min_quantity,
            unit=model.unit,
            location=model.location,
            status=SupplyStatus(model.status),
            price=model.price,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Supply) -> SupplyModel:
        return SupplyModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            category_id=entity.category_id,
            quantity=entity.quantity,
            min_quantity=entity.min_quantity,
            unit=entity.unit,
            location=entity.location,
            status=entity.status.value,
            price=entity.price,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

class SQLAlchemySupplyCategoryRepository(SupplyCategoryRepository):
    """SQLAlchemy 비품 카테고리 리포지토리 구현"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[SupplyCategory]:
        model = self.db.query(SupplyCategoryModel).filter(SupplyCategoryModel.id == id).first()
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SupplyCategory]:
        models = self.db.query(SupplyCategoryModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    def create(self, entity: SupplyCategory) -> SupplyCategory:
        model = self._entity_to_model(entity)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, entity: SupplyCategory) -> Optional[SupplyCategory]:
        model = self.db.query(SupplyCategoryModel).filter(SupplyCategoryModel.id == entity.id).first()
        if not model:
            return None
        
        model.name = entity.name
        model.description = entity.description
        
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def delete(self, id: int) -> bool:
        model = self.db.query(SupplyCategoryModel).filter(SupplyCategoryModel.id == id).first()
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
    
    def exists(self, id: int) -> bool:
        return self.db.query(SupplyCategoryModel).filter(SupplyCategoryModel.id == id).first() is not None
    
    def get_by_name(self, name: str) -> Optional[SupplyCategory]:
        model = self.db.query(SupplyCategoryModel).filter(SupplyCategoryModel.name == name).first()
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def name_exists(self, name: str) -> bool:
        return self.db.query(SupplyCategoryModel).filter(SupplyCategoryModel.name == name).first() is not None
    
    def get_with_supplies_count(self) -> List[dict]:
        from sqlalchemy import func
        
        result = self.db.query(
            SupplyCategoryModel.id,
            SupplyCategoryModel.name,
            SupplyCategoryModel.description,
            SupplyCategoryModel.created_at,
            func.count(SupplyModel.id).label('supplies_count')
        ).outerjoin(SupplyModel, SupplyCategoryModel.id == SupplyModel.category_id)\
         .group_by(SupplyCategoryModel.id).all()
        
        return [
            {
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'created_at': row.created_at,
                'supplies_count': row.supplies_count
            }
            for row in result
        ]
    
    def _model_to_entity(self, model: SupplyCategoryModel) -> SupplyCategory:
        return SupplyCategory(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at
        )
    
    def _entity_to_model(self, entity: SupplyCategory) -> SupplyCategoryModel:
        return SupplyCategoryModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at
        )
