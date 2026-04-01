"""
의존성 주입 컨테이너
Clean Architecture의 의존성 주입을 관리
"""

from typing import Dict, Any, Type, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')

class DIContainer:
    """의존성 주입 컨테이너"""
    
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, callable] = {}
        self._singletons: Dict[Type, Any] = {}
    
    def register_singleton(self, interface: Type[T], implementation: T) -> None:
        """싱글톤 서비스 등록"""
        self._singletons[interface] = implementation
    
    def register_factory(self, interface: Type[T], factory: callable) -> None:
        """팩토리 함수 등록"""
        self._factories[interface] = factory
    
    def register_transient(self, interface: Type[T], implementation: Type[T]) -> None:
        """매번 새 인스턴스 생성"""
        self._services[interface] = implementation
    
    def get(self, interface: Type[T]) -> T:
        """서비스 인스턴스 가져오기"""
        # 싱글톤 확인
        if interface in self._singletons:
            return self._singletons[interface]
        
        # 팩토리 확인
        if interface in self._factories:
            return self._factories[interface]()
        
        # 일반 서비스 확인
        if interface in self._services:
            implementation = self._services[interface]
            return implementation()
        
        raise ValueError(f"Service {interface} not registered")

# 전역 컨테이너 인스턴스
container = DIContainer()

def inject(interface: Type[T]) -> T:
    """의존성 주입 데코레이터"""
    return container.get(interface)

# 서비스 등록 함수
def setup_dependencies(db_session):
    """의존성 설정"""
    from ..infrastructure.repositories.sqlalchemy_supply_repository import (
        SQLAlchemySupplyRepository, SQLAlchemySupplyCategoryRepository
    )
    from ..infrastructure.services.sqlalchemy_inventory_service import SQLAlchemyInventoryService
    from ..application.use_cases.supply_use_cases import (
        CreateSupplyUseCase, GetSuppliesUseCase, UpdateSupplyUseCase,
        DeleteSupplyUseCase, GetLowStockAlertsUseCase
    )
    
    # 리포지토리 등록
    container.register_transient(
        SQLAlchemySupplyRepository,
        lambda: SQLAlchemySupplyRepository(db_session)
    )
    
    container.register_transient(
        SQLAlchemySupplyCategoryRepository,
        lambda: SQLAlchemySupplyCategoryRepository(db_session)
    )
    
    # 서비스 등록
    container.register_transient(
        SQLAlchemyInventoryService,
        lambda: SQLAlchemyInventoryService(db_session, container.get(SQLAlchemySupplyRepository))
    )
    
    # 유스케이스 등록
    container.register_transient(
        CreateSupplyUseCase,
        lambda: CreateSupplyUseCase(
            container.get(SQLAlchemySupplyRepository),
            container.get(SQLAlchemySupplyCategoryRepository),
            container.get(SQLAlchemyInventoryService)
        )
    )
    
    container.register_transient(
        GetSuppliesUseCase,
        lambda: GetSuppliesUseCase(container.get(SQLAlchemySupplyRepository))
    )
    
    container.register_transient(
        UpdateSupplyUseCase,
        lambda: UpdateSupplyUseCase(
            container.get(SQLAlchemySupplyRepository),
            container.get(SQLAlchemyInventoryService)
        )
    )
    
    container.register_transient(
        DeleteSupplyUseCase,
        lambda: DeleteSupplyUseCase(container.get(SQLAlchemySupplyRepository))
    )
    
    container.register_transient(
        GetLowStockAlertsUseCase,
        lambda: GetLowStockAlertsUseCase(container.get(SQLAlchemySupplyRepository))
    )
