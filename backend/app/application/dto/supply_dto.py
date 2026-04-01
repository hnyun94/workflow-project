from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal
from ...domain.entities.supply import Supply, SupplyCategory

@dataclass
class SupplyCategoryDto:
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    @classmethod
    def from_entity(cls, category: SupplyCategory) -> 'SupplyCategoryDto':
        return cls(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at
        )

@dataclass
class SupplyDto:
    id: int
    name: str
    description: Optional[str]
    category_id: int
    quantity: int
    min_quantity: int
    unit: str
    location: Optional[str]
    status: str
    price: Optional[Decimal]
    created_at: datetime
    updated_at: Optional[datetime]
    category: Optional[SupplyCategoryDto] = None
    
    @classmethod
    def from_entity(cls, supply: Supply, category: Optional[SupplyCategory] = None) -> 'SupplyDto':
        category_dto = None
        if category:
            category_dto = SupplyCategoryDto.from_entity(category)
        
        return cls(
            id=supply.id,
            name=supply.name,
            description=supply.description,
            category_id=supply.category_id,
            quantity=supply.quantity,
            min_quantity=supply.min_quantity,
            unit=supply.unit,
            location=supply.location,
            status=supply.status.value,
            price=supply.price,
            created_at=supply.created_at,
            updated_at=supply.updated_at,
            category=category_dto
        )

@dataclass
class CreateSupplyDto:
    name: str
    description: Optional[str]
    category_id: int
    quantity: int
    min_quantity: int
    unit: str
    location: Optional[str]
    price: Optional[Decimal]

@dataclass
class UpdateSupplyDto:
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = None
    min_quantity: Optional[int] = None
    unit: Optional[str] = None
    location: Optional[str] = None
    price: Optional[Decimal] = None

@dataclass
class SupplyListResponseDto:
    supplies: list[SupplyDto]
    total: int
    skip: int
    limit: int
