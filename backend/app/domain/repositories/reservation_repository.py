from typing import List, Optional
from datetime import datetime
from .base import Repository
from ..entities.reservation import Reservation
from ..enums.common import ReservationStatus

class ReservationRepository(Repository[Reservation]):
    """예약 리포지토리 인터페이스"""
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Reservation]:
        """사용자별 예약 조회"""
        pass
    
    @abstractmethod
    def get_by_supply(self, supply_id: int) -> List[Reservation]:
        """비품별 예약 조회"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: ReservationStatus) -> List[Reservation]:
        """상태별 예약 조회"""
        pass
    
    @abstractmethod
    def get_active_reservations(self) -> List[Reservation]:
        """활성 예약 조회"""
        pass
    
    @abstractmethod
    def get_overlapping_reservations(self, supply_id: int, start_date: datetime, end_date: datetime) -> List[Reservation]:
        """시간 중복 예약 조회"""
        pass
    
    @abstractmethod
    def get_pending_reservations(self) -> List[Reservation]:
        """대기 중 예약 조회"""
        pass
    
    @abstractmethod
    def update_status(self, reservation_id: int, status: ReservationStatus, approver_id: Optional[int] = None) -> Optional[Reservation]:
        """예약 상태 업데이트"""
        pass
