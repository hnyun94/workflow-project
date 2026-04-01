from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.reservation import ReservationStatus

class ReservationBase(BaseModel):
    supply_id: int
    quantity: int
    start_date: datetime
    end_date: datetime
    purpose: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    quantity: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    purpose: Optional[str] = None
    status: Optional[ReservationStatus] = None
    notes: Optional[str] = None

class Reservation(ReservationBase):
    id: int
    user_id: int
    status: ReservationStatus
    approved_by: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
