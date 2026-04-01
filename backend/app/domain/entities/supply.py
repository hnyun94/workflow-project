from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal
from ..enums.common import SupplyStatus

@dataclass
class SupplyCategory:
    """비품 카테고리 도메인 엔티티"""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """도메인 규칙 검증"""
        if not self.name:
            raise ValueError("Category name is required")
        if len(self.name) > 50:
            raise ValueError("Category name too long")

@dataclass
class Supply:
    """비품 도메인 엔티티"""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    category_id: int = 0
    quantity: int = 0
    min_quantity: int = 1
    unit: str = "개"
    location: Optional[str] = None
    status: SupplyStatus = SupplyStatus.AVAILABLE
    price: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """도메인 규칙 검증"""
        if not self.name:
            raise ValueError("Supply name is required")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.min_quantity < 0:
            raise ValueError("Minimum quantity cannot be negative")
        if self.category_id <= 0:
            raise ValueError("Invalid category ID")
        
        # 상태 자동 업데이트
        self._update_status()
    
    def _update_status(self):
        """재고 상태 자동 업데이트"""
        if self.quantity == 0:
            self.status = SupplyStatus.OUT_OF_STOCK
        elif self.quantity <= self.min_quantity:
            self.status = SupplyStatus.AVAILABLE  # 재고 부족 경고
        else:
            self.status = SupplyStatus.AVAILABLE
    
    def is_available(self) -> bool:
        """사용 가능 여부 확인"""
        return self.status == SupplyStatus.AVAILABLE and self.quantity > 0
    
    def is_low_stock(self) -> bool:
        """재고 부족 여부 확인"""
        return self.quantity <= self.min_quantity
    
    def is_out_of_stock(self) -> bool:
        """재고 없음 여부 확인"""
        return self.quantity == 0
    
    def add_stock(self, quantity: int) -> 'Supply':
        """재고 추가"""
        if quantity <= 0:
            raise ValueError("Quantity to add must be positive")
        
        self.quantity += quantity
        self._update_status()
        return self
    
    def remove_stock(self, quantity: int) -> 'Supply':
        """재고 차감"""
        if quantity <= 0:
            raise ValueError("Quantity to remove must be positive")
        
        if self.quantity < quantity:
            raise ValueError("Insufficient stock")
        
        self.quantity -= quantity
        self._update_status()
        return self
    
    def reserve(self, quantity: int) -> 'Supply':
        """비품 예약 (재고 차감)"""
        if quantity <= 0:
            raise ValueError("Quantity to reserve must be positive")
        
        if not self.is_available():
            raise ValueError("Supply not available for reservation")
        
        if self.quantity < quantity:
            raise ValueError("Insufficient stock for reservation")
        
        self.quantity -= quantity
        self._update_status()
        return self
    
    def release_reservation(self, quantity: int) -> 'Supply':
        """예약 해제 (재고 복귀)"""
        if quantity <= 0:
            raise ValueError("Quantity to release must be positive")
        
        self.quantity += quantity
        self._update_status()
        return self
    
    def update_location(self, new_location: str) -> 'Supply':
        """보관 위치 업데이트"""
        self.location = new_location
        return self
    
    def update_price(self, new_price: Decimal) -> 'Supply':
        """가격 업데이트"""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        
        self.price = new_price
        return self
