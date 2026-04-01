from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.reservation import Reservation as ReservationModel, ReservationStatus
from app.schemas.reservation import Reservation, ReservationCreate, ReservationUpdate
from app.services.reservation_service import ReservationService

router = APIRouter()

@router.get("/", response_model=List[Reservation])
async def get_reservations(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    reservation_service = ReservationService(db)
    
    # 일반 사용자는 자신의 예약만 볼 수 있음
    if current_user.role.value == "user":
        reservations = reservation_service.get_user_reservations(
            current_user.id, skip=skip, limit=limit, status=status
        )
    else:
        reservations = reservation_service.get_reservations(
            skip=skip, limit=limit, status=status
        )
    
    return reservations

@router.post("/", response_model=Reservation)
async def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    reservation_service = ReservationService(db)
    return reservation_service.create_reservation(reservation, current_user.id)

@router.get("/{reservation_id}", response_model=Reservation)
async def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    reservation_service = ReservationService(db)
    reservation = reservation_service.get_reservation(reservation_id)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # 권한 확인
    if (current_user.role.value == "user" and 
        reservation.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return reservation

@router.put("/{reservation_id}", response_model=Reservation)
async def update_reservation(
    reservation_id: int,
    reservation_update: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    reservation_service = ReservationService(db)
    reservation = reservation_service.get_reservation(reservation_id)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # 권한 확인
    if (current_user.role.value == "user" and 
        reservation.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # 상태 변경은 관리자/매니저만 가능
    if reservation_update.status and current_user.role.value not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions to change status")
    
    return reservation_service.update_reservation(reservation_id, reservation_update, current_user.id)

@router.delete("/{reservation_id}")
async def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    reservation_service = ReservationService(db)
    reservation = reservation_service.get_reservation(reservation_id)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # 권한 확인
    if (current_user.role.value == "user" and 
        reservation.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # 승인된 예약은 관리자만 취소 가능
    if (reservation.status == ReservationStatus.APPROVED and 
        current_user.role.value not in ["admin", "manager"]):
        raise HTTPException(status_code=403, detail="Cannot cancel approved reservation")
    
    success = reservation_service.cancel_reservation(reservation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel reservation")
    
    return {"message": "Reservation cancelled successfully"}
