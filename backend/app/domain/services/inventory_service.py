from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from ..entities.supply import Supply
from ..entities.transaction import SupplyTransaction
from ..entities.reservation import Reservation
from ..enums.common import TransactionType, SupplyStatus

class InventoryService(ABC):
    """재고 관리 도메인 서비스"""
    
    @abstractmethod
    def update_stock(self, supply_id: int, quantity_change: int, transaction_type: TransactionType, user_id: int, notes: str = "") -> Supply:
        """재고 업데이트"""
        pass
    
    @abstractmethod
    def check_low_stock(self, supply_id: int) -> bool:
        """재고 부족 확인"""
        pass
    
    @abstractmethod
    def is_available_for_reservation(self, supply_id: int, quantity: int, start_date: datetime, end_date: datetime) -> bool:
        """예약 가능 여부 확인"""
        pass
    
    @abstractmethod
    def get_low_stock_alerts(self) -> List[Supply]:
        """재고 부족 알림 목록"""
        pass
    
    @abstractmethod
    def reserve_supply(self, supply_id: int, quantity: int) -> Supply:
        """비품 예약 (재고 차감)"""
        pass
    
    @abstractmethod
    def release_reservation(self, supply_id: int, quantity: int) -> Supply:
        """예약 해제 (재고 복귀)"""
        pass
    
    @abstractmethod
    def create_transaction_record(self, supply_id: int, user_id: int, transaction_type: TransactionType, quantity: int, quantity_before: int, quantity_after: int, notes: str = "") -> SupplyTransaction:
        """거래 기록 생성"""
        pass
