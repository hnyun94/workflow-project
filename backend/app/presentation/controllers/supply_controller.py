from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...api.v1.endpoints.auth import get_current_user
from ...models.user import User as UserModel
from ...application.use_cases.supply_use_cases import (
    CreateSupplyUseCase, GetSuppliesUseCase, UpdateSupplyUseCase, 
    DeleteSupplyUseCase, GetLowStockAlertsUseCase,
    CreateSupplyRequest, GetSuppliesRequest, UpdateSupplyRequest
)
from ...infrastructure.repositories.sqlalchemy_supply_repository import (
    SQLAlchemySupplyRepository, SQLAlchemySupplyCategoryRepository
)
from ...infrastructure.services.sqlalchemy_inventory_service import SQLAlchemyInventoryService
from ...domain.enums.common import TransactionType

router = APIRouter()

# 의존성 주입 설정
def get_supply_repository(db: Session = Depends(get_db)) -> SQLAlchemySupplyRepository:
    return SQLAlchemySupplyRepository(db)

def get_category_repository(db: Session = Depends(get_db)) -> SQLAlchemySupplyCategoryRepository:
    return SQLAlchemySupplyCategoryRepository(db)

def get_inventory_service(db: Session = Depends(get_db), supply_repo = Depends(get_supply_repository)) -> SQLAlchemyInventoryService:
    return SQLAlchemyInventoryService(db, supply_repo)

# 유스케이스 의존성 주입
def get_create_supply_use_case(
    supply_repo = Depends(get_supply_repository),
    category_repo = Depends(get_category_repository),
    inventory_service = Depends(get_inventory_service)
) -> CreateSupplyUseCase:
    return CreateSupplyUseCase(supply_repo, category_repo, inventory_service)

def get_get_supplies_use_case(supply_repo = Depends(get_supply_repository)) -> GetSuppliesUseCase:
    return GetSuppliesUseCase(supply_repo)

def get_update_supply_use_case(
    supply_repo = Depends(get_supply_repository),
    inventory_service = Depends(get_inventory_service)
) -> UpdateSupplyUseCase:
    return UpdateSupplyUseCase(supply_repo, inventory_service)

def get_delete_supply_use_case(supply_repo = Depends(get_supply_repository)) -> DeleteSupplyUseCase:
    return DeleteSupplyUseCase(supply_repo)

def get_low_stock_alerts_use_case(supply_repo = Depends(get_supply_repository)) -> GetLowStockAlertsUseCase:
    return GetLowStockAlertsUseCase(supply_repo)

@router.get("/", response_model=List[dict])
async def get_supplies(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    use_case: GetSuppliesUseCase = Depends(get_get_supplies_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """비품 목록 조회"""
    request = GetSuppliesRequest(skip=skip, limit=limit, category_id=category_id, status=status)
    response = use_case.execute(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    
    return response.data

@router.get("/{supply_id}", response_model=dict)
async def get_supply(
    supply_id: int,
    use_case: GetSuppliesUseCase = Depends(get_get_supplies_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """비품 상세 조회"""
    # 단일 조회를 위한 임시 구현
    from ...infrastructure.repositories.sqlalchemy_supply_repository import SQLAlchemySupplyRepository
    from ...core.database import get_db
    
    db = next(get_db())
    repo = SQLAlchemySupplyRepository(db)
    supply = repo.get_by_id(supply_id)
    
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    
    from ...application.dto.supply_dto import SupplyDto
    return SupplyDto.from_entity(supply)

@router.post("/", response_model=dict)
async def create_supply(
    supply_data: dict,
    use_case: CreateSupplyUseCase = Depends(get_create_supply_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """비품 생성"""
    # 관리자 및 매니저만 생성 가능
    if current_user.role.value not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    request = CreateSupplyRequest(**supply_data)
    response = use_case.execute(request, current_user.id)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    
    return response.data

@router.put("/{supply_id}", response_model=dict)
async def update_supply(
    supply_id: int,
    supply_data: dict,
    use_case: UpdateSupplyUseCase = Depends(get_update_supply_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """비품 수정"""
    # 관리자 및 매니저만 수정 가능
    if current_user.role.value not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    request = UpdateSupplyRequest(supply_id=supply_id, **supply_data)
    response = use_case.execute(request, current_user.id)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    
    return response.data

@router.delete("/{supply_id}")
async def delete_supply(
    supply_id: int,
    use_case: DeleteSupplyUseCase = Depends(get_delete_supply_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """비품 삭제"""
    # 관리자만 삭제 가능
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    response = use_case.execute(supply_id)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    
    return {"message": "Supply deleted successfully"}

@router.get("/low-stock/alerts", response_model=List[dict])
async def get_low_stock_alerts(
    use_case: GetLowStockAlertsUseCase = Depends(get_low_stock_alerts_use_case),
    current_user: UserModel = Depends(get_current_user)
):
    """재고 부족 알림"""
    response = use_case.execute()
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    
    return response.data
