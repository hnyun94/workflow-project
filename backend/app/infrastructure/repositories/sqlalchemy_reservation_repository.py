from typing import List, Optional
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from datetime import datetime
from ...domain.repositories.reservation_repository import ReservationRepository
from ...domain.entities.reservation import Reservation
from ...domain.enums.common import ReservationStatus
from ...models.reservation import Reservation as ReservationModel

class SQLAlchemyReservationRepository(ReservationRepository):
    """SQLAlchemy 예약 리포지토리 구현"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[Reservation]:
        model = self.db.query(ReservationModel).filter(ReservationModel.id == id).first()
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Reservation]:
        models = self.db.query(ReservationModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    def create(self, entity: Reservation) -> Reservation:
        model = self._entity_to_model(entity)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def update(self, entity: Reservation) -> Optional[Reservation]:
        model = self.db.query(ReservationModel).filter(ReservationModel.id == entity.id).first()
        if not model:
            return None
        
        model.supply_id = entity.supply_id
        model.user_id = entity.user_id
        model.quantity = entity.quantity
        model.start_date = entity.start_date
        model.end_date = entity.end_date
        model.purpose = entity.purpose
        model.status = entity.status.value
        model.approved_by = entity.approved_by
        model.notes = entity.notes
        
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def delete(self, id: int) -> bool:
        model = self.db.query(ReservationModel).filter(ReservationModel.id == id).first()
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
    
    def exists(self, id: int) -> bool:
        return self.db.query(ReservationModel).filter(ReservationModel.id == id).first() is not None
    
    def get_by_user(self, user_id: int) -> List[Reservation]:
        models = self.db.query(ReservationModel).filter(ReservationModel.user_id == user_id).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_by_supply(self, supply_id: int) -> List[Reservation]:
        models = self.db.query(ReservationModel).filter(ReservationModel.supply_id == supply_id).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_by_status(self, status: ReservationStatus) -> List[Reservation]:
        models = self.db.query(ReservationModel).filter(ReservationModel.status == status.value).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_active_reservations(self) -> List[Reservation]:
        active_statuses = [ReservationStatus.PENDING, ReservationStatus.APPROVED]
        models = self.db.query(ReservationModel).filter(
            ReservationModel.status.in_([status.value for status in active_statuses])
        ).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_overlapping_reservations(self, supply_id: int, start_date: datetime, end_date: datetime) -> List[Reservation]:
        models = self.db.query(ReservationModel).filter(
            ReservationModel.supply_id == supply_id,
            ReservationModel.status.in_([ReservationStatus.PENDING.value, ReservationStatus.APPROVED.value]),
            ReservationModel.start_date < end_date,
            ReservationModel.end_date > start_date
        ).all()
        return [self._model_to_entity(model) for model in models]
    
    def get_pending_reservations(self) -> List[Reservation]:
        models = self.db.query(ReservationModel).filter(ReservationModel.status == ReservationStatus.PENDING.value).all()
        return [self._model_to_entity(model) for model in models]
    
    def update_status(self, reservation_id: int, status: ReservationStatus, approver_id: Optional[int] = None) -> Optional[Reservation]:
        model = self.db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
        if not model:
            return None
        
        model.status = status.value
        if approver_id:
            model.approved_by = approver_id
        
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)
    
    def _model_to_entity(self, model: ReservationModel) -> Reservation:
        return Reservation(
            id=model.id,
            supply_id=model.supply_id,
            user_id=model.user_id,
            quantity=model.quantity,
            start_date=model.start_date,
            end_date=model.end_date,
            purpose=model.purpose,
            status=ReservationStatus(model.status),
            approved_by=model.approved_by,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Reservation) -> ReservationModel:
        return ReservationModel(
            id=entity.id,
            supply_id=entity.supply_id,
            user_id=entity.user_id,
            quantity=entity.quantity,
            start_date=entity.start_date,
            end_date=entity.end_date,
            purpose=entity.purpose,
            status=entity.status.value,
            approved_by=entity.approved_by,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
