from typing import List
from sqlalchemy.orm import Session
from ...domain.services.inventory_service import InventoryService
from ...domain.entities.supply import Supply
from ...domain.entities.transaction import SupplyTransaction
from ...domain.repositories.supply_repository import SupplyRepository
from ...domain.enums.common import TransactionType

class SQLAlchemyInventoryService(InventoryService):
    """SQLAlchemy 재고 관리 서비스 구현"""
    
    def __init__(self, db: Session, supply_repository: SupplyRepository):
        self.db = db
        self.supply_repository = supply_repository
    
    def update_stock(self, supply_id: int, quantity_change: int, transaction_type: TransactionType, user_id: int, notes: str = "") -> Supply:
        supply = self.supply_repository.get_by_id(supply_id)
        if not supply:
            raise ValueError("Supply not found")
        
        old_quantity = supply.quantity
        new_quantity = old_quantity + quantity_change
        
        if new_quantity < 0:
            raise ValueError("Insufficient stock")
        
        # 거래 기록 생성
        self.create_transaction_record(
            supply_id=supply_id,
            user_id=user_id,
            transaction_type=transaction_type,
            quantity=abs(quantity_change),
            quantity_before=old_quantity,
            quantity_after=new_quantity,
            notes=notes
        )
        
        # 재고 업데이트
        supply.quantity = new_quantity
        supply._update_status()
        
        return self.supply_repository.update(supply)
    
    def check_low_stock(self, supply_id: int) -> bool:
        supply = self.supply_repository.get_by_id(supply_id)
        if not supply:
            return False
        
        return supply.is_low_stock()
    
    def is_available_for_reservation(self, supply_id: int, quantity: int, start_date, end_date) -> bool:
        supply = self.supply_repository.get_by_id(supply_id)
        if not supply:
            return False
        
        if not supply.is_available():
            return False
        
        if supply.quantity < quantity:
            return False
        
        # TODO: 예약 충돌 확인 로직 추가
        return True
    
    def get_low_stock_alerts(self) -> List[Supply]:
        return self.supply_repository.get_low_stock_supplies()
    
    def reserve_supply(self, supply_id: int, quantity: int) -> Supply:
        supply = self.supply_repository.get_by_id(supply_id)
        if not supply:
            raise ValueError("Supply not found")
        
        supply.reserve(quantity)
        return self.supply_repository.update(supply)
    
    def release_reservation(self, supply_id: int, quantity: int) -> Supply:
        supply = self.supply_repository.get_by_id(supply_id)
        if not supply:
            raise ValueError("Supply not found")
        
        supply.release_reservation(quantity)
        return self.supply_repository.update(supply)
    
    def create_transaction_record(self, supply_id: int, user_id: int, transaction_type: TransactionType, quantity: int, quantity_before: int, quantity_after: int, notes: str = "") -> SupplyTransaction:
        from ...models.supply import SupplyTransaction as SupplyTransactionModel
        
        transaction = SupplyTransactionModel(
            supply_id=supply_id,
            user_id=user_id,
            transaction_type=transaction_type.value,
            quantity=quantity,
            quantity_before=quantity_before,
            quantity_after=quantity_after,
            notes=notes
        )
        
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        
        return SupplyTransaction(
            id=transaction.id,
            supply_id=transaction.supply_id,
            user_id=transaction.user_id,
            transaction_type=TransactionType(transaction.transaction_type),
            quantity=transaction.quantity,
            quantity_before=transaction.quantity_before,
            quantity_after=transaction.quantity_after,
            notes=transaction.notes,
            created_at=transaction.created_at
        )
