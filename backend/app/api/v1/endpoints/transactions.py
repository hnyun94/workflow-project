from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.supply import SupplyTransaction as SupplyTransactionModel
from app.schemas.transaction import SupplyTransaction, SupplyTransactionCreate
from app.services.supply_service import SupplyService
from app.models.supply import TransactionType

router = APIRouter()

@router.get("/", response_model=List[SupplyTransaction])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    supply_id: int = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    query = db.query(SupplyTransactionModel)
    
    if supply_id:
        query = query.filter(SupplyTransactionModel.supply_id == supply_id)
    
    return query.order_by(SupplyTransactionModel.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=SupplyTransaction)
async def create_transaction(
    transaction: SupplyTransactionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    supply_service = SupplyService(db)
    
    try:
        # 재고 업데이트
        if transaction.transaction_type == TransactionType.IN:
            updated_supply = supply_service.update_stock(
                transaction.supply_id, 
                transaction.quantity, 
                TransactionType.IN, 
                current_user.id, 
                transaction.notes or "입고"
            )
        elif transaction.transaction_type == TransactionType.OUT:
            updated_supply = supply_service.update_stock(
                transaction.supply_id, 
                -transaction.quantity, 
                TransactionType.OUT, 
                current_user.id, 
                transaction.notes or "출고"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid transaction type")
        
        if not updated_supply:
            raise HTTPException(status_code=404, detail="Supply not found")
        
        # 트랜잭션 기록은 service에서 자동 생성
        # 최신 트랜잭션 반환
        latest_transaction = db.query(SupplyTransactionModel).filter(
            SupplyTransactionModel.supply_id == transaction.supply_id
        ).order_by(SupplyTransactionModel.created_at.desc()).first()
        
        return latest_transaction
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Transaction failed")
