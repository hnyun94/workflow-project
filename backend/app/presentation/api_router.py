"""
API 라우터 모음
Clean Architecture 기반의 API 엔드포인트 등록
"""

from fastapi import APIRouter
from .controllers.auth_controller import router as auth_router
from .controllers.supply_controller import router as supply_router

api_router = APIRouter()

# 인증 관련 엔드포인트
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["authentication"]
)

# 비품 관리 엔드포인트
api_router.include_router(
    supply_router,
    prefix="/supplies",
    tags=["supplies"]
)

# TODO: 다른 컨트롤러들 추가
# api_router.include_router(reservation_router, prefix="/reservations", tags=["reservations"])
# api_router.include_router(user_router, prefix="/users", tags=["users"])
# api_router.include_router(category_router, prefix="/categories", tags=["categories"])
# api_router.include_router(transaction_router, prefix="/transactions", tags=["transactions"])
