from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.supply import TransactionType

class SupplyTransactionBase(BaseModel):
    supply_id: int
    transaction_type: TransactionType
    quantity: int
    notes: Optional[str] = None

class SupplyTransactionCreate(SupplyTransactionBase):
    pass

class SupplyTransaction(SupplyTransactionBase):
    id: int
    user_id: int
    quantity_before: Optional[int] = None
    quantity_after: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
