from typing import List, Optional
from .base import UseCase, UseCaseRequest, UseCaseResponse, SuccessResponse, ErrorResponse
from ..dto.supply_dto import SupplyDto, CreateSupplyDto, UpdateSupplyDto
from ...domain.entities.supply import Supply
from ...domain.repositories.supply_repository import SupplyRepository, SupplyCategoryRepository
from ...domain.services.inventory_service import InventoryService
from ...domain.enums.common import SupplyStatus

class CreateSupplyRequest(UseCaseRequest):
    def __init__(self, name: str, description: str, category_id: int, quantity: int, 
                 min_quantity: int, unit: str, location: str, price: float):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.quantity = quantity
        self.min_quantity = min_quantity
        self.unit = unit
        self.location = location
        self.price = price

class CreateSupplyUseCase(UseCase):
    """비품 생성 유스케이스"""
    
    def __init__(self, supply_repository: SupplyRepository, 
                 category_repository: SupplyCategoryRepository,
                 inventory_service: InventoryService):
        self.supply_repository = supply_repository
        self.category_repository = category_repository
        self.inventory_service = inventory_service
    
    def execute(self, request: CreateSupplyRequest, user_id: int) -> UseCaseResponse:
        try:
            # 비즈니스 로직 검증
            if not self.category_repository.get_by_id(request.category_id):
                return ErrorResponse("Invalid category", "Category not found")
            
            if request.quantity < 0:
                return ErrorResponse("Invalid quantity", "Quantity cannot be negative")
            
            if request.min_quantity < 0:
                return ErrorResponse("Invalid min_quantity", "Minimum quantity cannot be negative")
            
            # 엔티티 생성
            supply = Supply(
                name=request.name,
                description=request.description,
                category_id=request.category_id,
                quantity=request.quantity,
                min_quantity=request.min_quantity,
                unit=request.unit,
                location=request.location,
                price=request.price
            )
            
            # 저장
            created_supply = self.supply_repository.create(supply)
            
            # 초기 재고 입고 기록
            if created_supply.quantity > 0:
                self.inventory_service.create_transaction_record(
                    supply_id=created_supply.id,
                    user_id=user_id,
                    transaction_type="in",
                    quantity=created_supply.quantity,
                    quantity_before=0,
                    quantity_after=created_supply.quantity,
                    notes="초기 재고 등록"
                )
            
            return SuccessResponse(SupplyDto.from_entity(created_supply), "Supply created successfully")
            
        except Exception as e:
            return ErrorResponse(str(e), "Failed to create supply")

class GetSuppliesRequest(UseCaseRequest):
    def __init__(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, status: Optional[str] = None):
        self.skip = skip
        self.limit = limit
        self.category_id = category_id
        self.status = status

class GetSuppliesUseCase(UseCase):
    """비품 목록 조회 유스케이스"""
    
    def __init__(self, supply_repository: SupplyRepository):
        self.supply_repository = supply_repository
    
    def execute(self, request: GetSuppliesRequest) -> UseCaseResponse:
        try:
            if request.category_id:
                supplies = self.supply_repository.get_by_category(request.category_id)
            elif request.status:
                supplies = self.supply_repository.get_by_status(SupplyStatus(request.status))
            else:
                supplies = self.supply_repository.get_all(request.skip, request.limit)
            
            supply_dtos = [SupplyDto.from_entity(supply) for supply in supplies]
            return SuccessResponse(supply_dtos, "Supplies retrieved successfully")
            
        except Exception as e:
            return ErrorResponse(str(e), "Failed to retrieve supplies")

class UpdateSupplyRequest(UseCaseRequest):
    def __init__(self, supply_id: int, name: Optional[str] = None, description: Optional[str] = None,
                 category_id: Optional[int] = None, quantity: Optional[int] = None,
                 min_quantity: Optional[int] = None, unit: Optional[str] = None,
                 location: Optional[str] = None, price: Optional[float] = None):
        self.supply_id = supply_id
        self.name = name
        self.description = description
        self.category_id = category_id
        self.quantity = quantity
        self.min_quantity = min_quantity
        self.unit = unit
        self.location = location
        self.price = price

class UpdateSupplyUseCase(UseCase):
    """비품 수정 유스케이스"""
    
    def __init__(self, supply_repository: SupplyRepository, inventory_service: InventoryService):
        self.supply_repository = supply_repository
        self.inventory_service = inventory_service
    
    def execute(self, request: UpdateSupplyRequest, user_id: int) -> UseCaseResponse:
        try:
            supply = self.supply_repository.get_by_id(request.supply_id)
            if not supply:
                return ErrorResponse("Supply not found", "Supply not found")
            
            # 필드 업데이트
            if request.name is not None:
                supply.name = request.name
            if request.description is not None:
                supply.description = request.description
            if request.category_id is not None:
                supply.category_id = request.category_id
            if request.quantity is not None:
                old_quantity = supply.quantity
                supply.quantity = request.quantity
                
                # 수량 변경 시 거래 기록
                if old_quantity != request.quantity:
                    quantity_change = request.quantity - old_quantity
                    transaction_type = "in" if quantity_change > 0 else "out"
                    
                    self.inventory_service.create_transaction_record(
                        supply_id=supply.id,
                        user_id=user_id,
                        transaction_type=transaction_type,
                        quantity=abs(quantity_change),
                        quantity_before=old_quantity,
                        quantity_after=request.quantity,
                        notes="재고 수동 조정"
                    )
            
            if request.min_quantity is not None:
                supply.min_quantity = request.min_quantity
            if request.unit is not None:
                supply.unit = request.unit
            if request.location is not None:
                supply.location = request.location
            if request.price is not None:
                supply.price = request.price
            
            # 상태 자동 업데이트
            supply._update_status()
            
            updated_supply = self.supply_repository.update(supply)
            return SuccessResponse(SupplyDto.from_entity(updated_supply), "Supply updated successfully")
            
        except Exception as e:
            return ErrorResponse(str(e), "Failed to update supply")

class DeleteSupplyUseCase(UseCase):
    """비품 삭제 유스케이스"""
    
    def __init__(self, supply_repository: SupplyRepository):
        self.supply_repository = supply_repository
    
    def execute(self, supply_id: int) -> UseCaseResponse:
        try:
            success = self.supply_repository.delete(supply_id)
            if not success:
                return ErrorResponse("Supply not found", "Supply not found")
            
            return SuccessResponse(None, "Supply deleted successfully")
            
        except Exception as e:
            return ErrorResponse(str(e), "Failed to delete supply")

class GetLowStockAlertsUseCase(UseCase):
    """재고 부족 알림 조회 유스케이스"""
    
    def __init__(self, supply_repository: SupplyRepository):
        self.supply_repository = supply_repository
    
    def execute(self) -> UseCaseResponse:
        try:
            low_stock_supplies = self.supply_repository.get_low_stock_supplies()
            supply_dtos = [SupplyDto.from_entity(supply) for supply in low_stock_supplies]
            return SuccessResponse(supply_dtos, "Low stock alerts retrieved successfully")
            
        except Exception as e:
            return ErrorResponse(str(e), "Failed to retrieve low stock alerts")
