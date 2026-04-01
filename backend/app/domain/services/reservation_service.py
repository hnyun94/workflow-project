from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from ..entities.reservation import Reservation
from ..entities.supply import Supply
from ..enums.common import ReservationStatus

class ReservationDomainService(ABC):
    """예약 도메인 서비스"""
    
    @abstractmethod
    def create_reservation(self, reservation_data: dict, user_id: int) -> Reservation:
        """예약 생성"""
        pass
    
    @abstractmethod
    def approve_reservation(self, reservation_id: int, approver_id: int) -> Reservation:
        """예약 승인"""
        pass
    
    @abstractmethod
    def reject_reservation(self, reservation_id: int, approver_id: int, reason: str = None) -> Reservation:
        """예약 거절"""
        pass
    
    @abstractmethod
    def cancel_reservation(self, reservation_id: int, user_id: int) -> bool:
        """예약 취소"""
        pass
    
    @abstractmethod
    def complete_reservation(self, reservation_id: int) -> Reservation:
        """예약 완료"""
        pass
    
    @abstractmethod
    def validate_reservation_period(self, supply_id: int, start_date: datetime, end_date: datetime) -> bool:
        """예약 기간 유효성 검증"""
        pass
    
    @abstractmethod
    def check_reservation_conflicts(self, supply_id: int, start_date: datetime, end_date: datetime, exclude_reservation_id: int = None) -> List[Reservation]:
        """예약 충돌 확인"""
        pass
    
    @abstractmethod
    def get_upcoming_reservations(self, user_id: int) -> List[Reservation]:
        """다가오는 예약 조회"""
        pass
    
    @abstractmethod
    def get_overdue_reservations(self) -> List[Reservation]:
        """연체 예약 조회"""
        pass
