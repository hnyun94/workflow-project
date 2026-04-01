from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, supplies, categories, transactions, reservations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(supplies.router, prefix="/supplies", tags=["supplies"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
