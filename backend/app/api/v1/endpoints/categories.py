from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.supply import SupplyCategory as SupplyCategoryModel
from app.schemas.supply import SupplyCategory, SupplyCategoryCreate

router = APIRouter()

@router.get("/", response_model=List[SupplyCategory])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    categories = db.query(SupplyCategoryModel).offset(skip).limit(limit).all()
    return categories

@router.post("/", response_model=SupplyCategory)
async def create_category(
    category: SupplyCategoryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 관리자 및 매니저만 생성 가능
    if current_user.role.value not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_category = SupplyCategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/{category_id}", response_model=SupplyCategory)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    category = db.query(SupplyCategoryModel).filter(SupplyCategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
