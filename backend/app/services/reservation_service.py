from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.reservation import Reservation as ReservationModel, ReservationStatus
from app.models.supply import Supply as SupplyModel, SupplyStatus
from app.schemas.reservation import ReservationCreate, ReservationUpdate

class ReservationService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_reservations(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[ReservationModel]:
        query = self.db.query(ReservationModel)
        
        if status:
            query = query.filter(ReservationModel.status == status)
        
        return query.order_by(ReservationModel.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_user_reservations(self, user_id: int, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[ReservationModel]:
        query = self.db.query(ReservationModel).filter(ReservationModel.user_id == user_id)
        
        if status:
            query = query.filter(ReservationModel.status == status)
        
        return query.order_by(ReservationModel.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_reservation(self, reservation_id: int) -> Optional[ReservationModel]:
        return self.db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    
    def create_reservation(self, reservation: ReservationCreate, user_id: int) -> ReservationModel:
        # 비품 존재 확인
        supply = self.db.query(SupplyModel).filter(SupplyModel.id == reservation.supply_id).first()
        if not supply:
            raise ValueError("Supply not found")
        
        # 재고 확인
        if supply.quantity < reservation.quantity:
            raise ValueError("Insufficient stock")
        
        # 예약 기간 중복 확인
        overlapping = self.db.query(ReservationModel).filter(
            ReservationModel.supply_id == reservation.supply_id,
            ReservationModel.status.in_([ReservationStatus.PENDING, ReservationStatus.APPROVED]),
            ReservationModel.start_date <= reservation.end_date,
            ReservationModel.end_date >= reservation.start_date
        ).first()
        
        if overlapping:
            raise ValueError("Supply already reserved for this period")
        
        db_reservation = ReservationModel(
            **reservation.dict(),
            user_id=user_id
        )
        
        self.db.add(db_reservation)
        self.db.commit()
        self.db.refresh(db_reservation)
        
        return db_reservation
    
    def update_reservation(self, reservation_id: int, reservation_update: ReservationUpdate, user_id: int) -> Optional[ReservationModel]:
        db_reservation = self.get_reservation(reservation_id)
        if not db_reservation:
            return None
        
        update_data = reservation_update.dict(exclude_unset=True)
        
        # 상태 변경 시 처리
        if "status" in update_data:
            new_status = update_data["status"]
            
            if new_status == ReservationStatus.APPROVED:
                # 예약 승인 시 재고 확인 및 차감
                supply = self.db.query(SupplyModel).filter(SupplyModel.id == db_reservation.supply_id).first()
                if supply.quantity < db_reservation.quantity:
                    raise ValueError("Insufficient stock for approval")
                
                # 재고 차감
                supply.quantity -= db_reservation.quantity
                if supply.quantity == 0:
                    supply.status = SupplyStatus.OUT_OF_STOCK
                elif supply.quantity <= supply.min_quantity:
                    supply.status = SupplyStatus.AVAILABLE
                
                db_reservation.approved_by = user_id
                
            elif new_status == ReservationStatus.COMPLETED:
                # 예약 완료 시 재고 복귀 (반납)
                supply = self.db.query(SupplyModel).filter(SupplyModel.id == db_reservation.supply_id).first()
                supply.quantity += db_reservation.quantity
                supply.status = SupplyStatus.AVAILABLE
                
            elif new_status == ReservationStatus.CANCELLED:
                # 예약 취소 시 (승인된 경우) 재고 복귀
                if db_reservation.status == ReservationStatus.APPROVED:
                    supply = self.db.query(SupplyModel).filter(SupplyModel.id == db_reservation.supply_id).first()
                    supply.quantity += db_reservation.quantity
                    supply.status = SupplyStatus.AVAILABLE
        
        # 필드 업데이트
        for field, value in update_data.items():
            setattr(db_reservation, field, value)
        
        self.db.commit()
        self.db.refresh(db_reservation)
        return db_reservation
    
    def cancel_reservation(self, reservation_id: int, user_id: int) -> bool:
        db_reservation = self.get_reservation(reservation_id)
        if not db_reservation:
            return False
        
        # 승인된 예약만 재고 복귀
        if db_reservation.status == ReservationStatus.APPROVED:
            supply = self.db.query(SupplyModel).filter(SupplyModel.id == db_reservation.supply_id).first()
            supply.quantity += db_reservation.quantity
            supply.status = SupplyStatus.AVAILABLE
        
        db_reservation.status = ReservationStatus.CANCELLED
        self.db.commit()
        return True
