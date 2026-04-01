from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..enums.common import ReservationStatus

@dataclass
class Reservation:
    """예약 도메인 엔티티"""
    id: Optional[int] = None
    supply_id: int = 0
    user_id: int = 0
    quantity: int = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    purpose: Optional[str] = None
    status: ReservationStatus = ReservationStatus.PENDING
    approved_by: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """도메인 규칙 검증"""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.supply_id <= 0:
            raise ValueError("Invalid supply ID")
        if self.user_id <= 0:
            raise ValueError("Invalid user ID")
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValueError("Start date must be before end date")
    
    def can_be_approved(self) -> bool:
        """승인 가능 여부 확인"""
        return self.status == ReservationStatus.PENDING
    
    def can_be_cancelled(self) -> bool:
        """취소 가능 여부 확인"""
        return self.status in [ReservationStatus.PENDING, ReservationStatus.APPROVED]
    
    def can_be_completed(self) -> bool:
        """완료 가능 여부 확인"""
        return self.status == ReservationStatus.APPROVED
    
    def approve(self, approver_id: int) -> 'Reservation':
        """예약 승인"""
        if not self.can_be_approved():
            raise ValueError("Reservation cannot be approved")
        
        self.status = ReservationStatus.APPROVED
        self.approved_by = approver_id
        return self
    
    def reject(self, approver_id: int, reason: str = None) -> 'Reservation':
        """예약 거절"""
        if not self.can_be_approved():
            raise ValueError("Reservation cannot be rejected")
        
        self.status = ReservationStatus.REJECTED
        self.approved_by = approver_id
        if reason:
            self.notes = reason
        return self
    
    def cancel(self, user_id: int, reason: str = None) -> 'Reservation':
        """예약 취소"""
        if not self.can_be_cancelled():
            raise ValueError("Reservation cannot be cancelled")
        
        self.status = ReservationStatus.CANCELLED
        if reason:
            self.notes = reason
        return self
    
    def complete(self) -> 'Reservation':
        """예약 완료"""
        if not self.can_be_completed():
            raise ValueError("Reservation cannot be completed")
        
        self.status = ReservationStatus.COMPLETED
        return self
    
    def is_active(self) -> bool:
        """활성 예약 여부 확인"""
        return self.status in [ReservationStatus.PENDING, ReservationStatus.APPROVED]
    
    def overlaps_with(self, other_start: datetime, other_end: datetime) -> bool:
        """시간 중복 확인"""
        if not self.start_date or not self.end_date:
            return False
        
        return not (self.end_date <= other_start or self.start_date >= other_end)
