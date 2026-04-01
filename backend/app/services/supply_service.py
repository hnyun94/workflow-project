from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.supply import Supply as SupplyModel, SupplyCategory, SupplyTransaction, TransactionType, SupplyStatus
from app.schemas.supply import SupplyCreate, SupplyUpdate, Supply
from app.schemas.transaction import SupplyTransactionCreate

class SupplyService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_supplies(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, status: Optional[str] = None) -> List[SupplyModel]:
        query = self.db.query(SupplyModel)
        
        if category_id:
            query = query.filter(SupplyModel.category_id == category_id)
        if status:
            query = query.filter(SupplyModel.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def get_supply(self, supply_id: int) -> Optional[SupplyModel]:
        return self.db.query(SupplyModel).filter(SupplyModel.id == supply_id).first()
    
    def create_supply(self, supply: SupplyCreate, user_id: int) -> SupplyModel:
        db_supply = SupplyModel(**supply.dict())
        
        # 상태 설정
        if db_supply.quantity == 0:
            db_supply.status = "out_of_stock"
        elif db_supply.quantity <= db_supply.min_quantity:
            db_supply.status = "available"  # 재고 부족 경고 필요
        else:
            db_supply.status = "available"
        
        self.db.add(db_supply)
        self.db.commit()
        self.db.refresh(db_supply)
        
        # 초기 재고 입고 기록
        if db_supply.quantity > 0:
            transaction = SupplyTransaction(
                supply_id=db_supply.id,
                user_id=user_id,
                transaction_type=TransactionType.IN,
                quantity=db_supply.quantity,
                quantity_before=0,
                quantity_after=db_supply.quantity,
                notes="초기 재고 등록"
            )
            self.db.add(transaction)
            self.db.commit()
        
        return db_supply
    
    def update_supply(self, supply_id: int, supply_update: SupplyUpdate, user_id: int) -> Optional[SupplyModel]:
        db_supply = self.get_supply(supply_id)
        if not db_supply:
            return None
        
        update_data = supply_update.dict(exclude_unset=True)
        
        # 수량 변경 시 트랜잭션 기록
        if "quantity" in update_data:
            old_quantity = db_supply.quantity
            new_quantity = update_data["quantity"]
            
            # 수량 변경 트랜잭션
            if old_quantity != new_quantity:
                transaction_type = TransactionType.IN if new_quantity > old_quantity else TransactionType.OUT
                transaction = SupplyTransaction(
                    supply_id=db_supply.id,
                    user_id=user_id,
                    transaction_type=transaction_type,
                    quantity=abs(new_quantity - old_quantity),
                    quantity_before=old_quantity,
                    quantity_after=new_quantity,
                    notes="재고 수동 조정"
                )
                self.db.add(transaction)
        
        # 필드 업데이트
        for field, value in update_data.items():
            setattr(db_supply, field, value)
        
        # 상태 자동 업데이트
        if "quantity" in update_data:
            if db_supply.quantity == 0:
                db_supply.status = "out_of_stock"
            elif db_supply.quantity <= db_supply.min_quantity:
                db_supply.status = "available"
            else:
                db_supply.status = "available"
        
        self.db.commit()
        self.db.refresh(db_supply)
        return db_supply
    
    def delete_supply(self, supply_id: int) -> bool:
        db_supply = self.get_supply(supply_id)
        if not db_supply:
            return False
        
        self.db.delete(db_supply)
        self.db.commit()
        return True
    
    def get_low_stock_alerts(self) -> List[SupplyModel]:
        return self.db.query(SupplyModel).filter(
            SupplyModel.quantity <= SupplyModel.min_quantity
        ).all()
    
    def update_stock(self, supply_id: int, quantity_change: int, transaction_type: TransactionType, user_id: int, notes: str = "") -> Optional[SupplyModel]:
        db_supply = self.get_supply(supply_id)
        if not db_supply:
            return None
        
        old_quantity = db_supply.quantity
        new_quantity = old_quantity + quantity_change
        
        if new_quantity < 0:
            raise ValueError("Insufficient stock")
        
        # 트랜잭션 기록
        transaction = SupplyTransaction(
            supply_id=db_supply.id,
            user_id=user_id,
            transaction_type=transaction_type,
            quantity=abs(quantity_change),
            quantity_before=old_quantity,
            quantity_after=new_quantity,
            notes=notes
        )
        self.db.add(transaction)
        
        # 재고 업데이트
        db_supply.quantity = new_quantity
        
        # 상태 업데이트
        if new_quantity == 0:
            db_supply.status = "out_of_stock"
        elif new_quantity <= db_supply.min_quantity:
            db_supply.status = "available"
        else:
            db_supply.status = "available"
        
        self.db.commit()
        self.db.refresh(db_supply)
        return db_supply
