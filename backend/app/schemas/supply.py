from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class SupplyCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class SupplyCategoryCreate(SupplyCategoryBase):
    pass

class SupplyCategory(SupplyCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SupplyBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    quantity: int = 0
    min_quantity: int = 1
    unit: str = "개"
    location: Optional[str] = None
    price: Optional[Decimal] = None

class SupplyCreate(SupplyBase):
    pass

class SupplyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = None
    min_quantity: Optional[int] = None
    unit: Optional[str] = None
    location: Optional[str] = None
    price: Optional[Decimal] = None

class Supply(SupplyBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[SupplyCategory] = None
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        data = {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "category_id": obj.category_id,
            "quantity": obj.quantity,
            "min_quantity": obj.min_quantity,
            "unit": obj.unit,
            "location": obj.location,
            "price": obj.price,
            "status": obj.status.value if hasattr(obj.status, 'value') else str(obj.status),
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
            "category": obj.category
        }
        return cls(**data)
