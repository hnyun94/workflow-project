from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..enums.common import TransactionType

@dataclass
class SupplyTransaction:
    """비품 거래 도메인 엔티티"""
    id: Optional[int] = None
    supply_id: int = 0
    user_id: int = 0
    transaction_type: TransactionType = TransactionType.IN
    quantity: int = 0
    quantity_before: Optional[int] = None
    quantity_after: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """도메인 규칙 검증"""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.supply_id <= 0:
            raise ValueError("Invalid supply ID")
        if self.user_id <= 0:
            raise ValueError("Invalid user ID")
        
        # 수량 변경 계산
        if self.transaction_type == TransactionType.OUT:
            self.quantity = -abs(self.quantity)
        else:
            self.quantity = abs(self.quantity)
    
    def is_in_transaction(self) -> bool:
        """입고 거래 여부"""
        return self.transaction_type == TransactionType.IN
    
    def is_out_transaction(self) -> bool:
        """출고 거래 여부"""
        return self.transaction_type == TransactionType.OUT
    
    def is_reserve_transaction(self) -> bool:
        """예약 거래 여부"""
        return self.transaction_type == TransactionType.RESERVE
    
    def get_quantity_change(self) -> int:
        """수량 변화량 반환"""
        if self.is_out_transaction():
            return -abs(self.quantity)
        return abs(self.quantity)
    
    def set_quantity_before_after(self, before: int, after: int) -> 'SupplyTransaction':
        """거래 전후 수량 설정"""
        self.quantity_before = before
        self.quantity_after = after
        return self
