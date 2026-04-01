from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.supply import Supply as SupplyModel, SupplyStatus
from app.schemas.supply import Supply, SupplyCreate, SupplyUpdate
from app.services.supply_service import SupplyService

router = APIRouter()

@router.get("/", response_model=List[Supply])
async def get_supplies(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    supply_service = SupplyService(db)
    supplies = supply_service.get_supplies(skip=skip, limit=limit, category_id=category_id, status=status)
    return supplies

@router.get("/{supply_id}", response_model=Supply)
async def get_supply(
    supply_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    supply_service = SupplyService(db)
    supply = supply_service.get_supply(supply_id)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return supply

@router.post("/", response_model=Supply)
async def create_supply(
    supply: SupplyCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 관리자 및 매니저만 생성 가능
    if current_user.role.value not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    supply_service = SupplyService(db)
    return supply_service.create_supply(supply, current_user.id)

@router.put("/{supply_id}", response_model=Supply)
async def update_supply(
    supply_id: int,
    supply_update: SupplyUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 관리자 및 매니저만 수정 가능
    if current_user.role.value not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    supply_service = SupplyService(db)
    supply = supply_service.update_supply(supply_id, supply_update, current_user.id)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return supply

@router.delete("/{supply_id}")
async def delete_supply(
    supply_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 관리자만 삭제 가능
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    supply_service = SupplyService(db)
    success = supply_service.delete_supply(supply_id)
    if not success:
        raise HTTPException(status_code=404, detail="Supply not found")
    return {"message": "Supply deleted successfully"}

@router.get("/low-stock/alerts")
async def get_low_stock_alerts(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    supply_service = SupplyService(db)
    return supply_service.get_low_stock_alerts()
