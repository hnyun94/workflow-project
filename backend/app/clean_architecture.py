"""
Clean Architecture 구조 정의

도메인 계층 (Domain Layer)
- 엔티티 (Entities)
- 값 객체 (Value Objects)
- 도메인 서비스 (Domain Services)
- 리포지토리 인터페이스 (Repository Interfaces)

애플리케이션 계층 (Application Layer)
- 유스케이스 (Use Cases)
- 유스케이스 인터페이스 (Use Case Interfaces)
- 애플리케이션 서비스 (Application Services)

인프라스트럭처 계층 (Infrastructure Layer)
- 리포지토리 구현 (Repository Implementations)
- 외부 API 클라이언트 (External API Clients)
- 데이터베이스 구현 (Database Implementations)

프레젠테이션 계층 (Presentation Layer)
- API 컨트롤러 (API Controllers)
- DTO (Data Transfer Objects)
- 미들웨어 (Middleware)
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# 도메인 계층 (Domain Layer)

class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class SupplyStatus(Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class TransactionType(Enum):
    IN = "in"
    OUT = "out"
    RESERVE = "reserve"

class ReservationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# 도메인 엔티티 (Domain Entities)
@dataclass
class UserEntity:
    id: Optional[int] = None
    email: str = ""
    username: str = ""
    department: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class SupplyCategoryEntity:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class SupplyEntity:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    category_id: int = 0
    quantity: int = 0
    min_quantity: int = 1
    unit: str = "개"
    location: Optional[str] = None
    status: SupplyStatus = SupplyStatus.AVAILABLE
    price: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class SupplyTransactionEntity:
    id: Optional[int] = None
    supply_id: int = 0
    user_id: int = 0
    transaction_type: TransactionType = TransactionType.IN
    quantity: int = 0
    quantity_before: Optional[int] = None
    quantity_after: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class ReservationEntity:
    id: Optional[int] = None
    supply_id: int = 0
    user_id: int = 0
    quantity: int = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    purpose: Optional[str] = None
    status: ReservationStatus = ReservationStatus.PENDING
    approved_by: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# 리포지토리 인터페이스 (Repository Interfaces)
T = TypeVar('T')

class Repository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> Optional[T]:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

class UserRepository(Repository[UserEntity]):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    def get_by_role(self, role: UserRole) -> List[UserEntity]:
        pass

class SupplyRepository(Repository[SupplyEntity]):
    @abstractmethod
    def get_by_category(self, category_id: int) -> List[SupplyEntity]:
        pass
    
    @abstractmethod
    def get_by_status(self, status: SupplyStatus) -> List[SupplyEntity]:
        pass
    
    @abstractmethod
    def get_low_stock_supplies(self) -> List[SupplyEntity]:
        pass

class SupplyCategoryRepository(Repository[SupplyCategoryEntity]):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[SupplyCategoryEntity]:
        pass

class ReservationRepository(Repository[ReservationEntity]):
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[ReservationEntity]:
        pass
    
    @abstractmethod
    def get_by_status(self, status: ReservationStatus) -> List[ReservationEntity]:
        pass
    
    @abstractmethod
    def get_overlapping_reservations(self, supply_id: int, start_date: datetime, end_date: datetime) -> List[ReservationEntity]:
        pass

class TransactionRepository(Repository[SupplyTransactionEntity]):
    @abstractmethod
    def get_by_supply(self, supply_id: int) -> List[SupplyTransactionEntity]:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[SupplyTransactionEntity]:
        pass

# 도메인 서비스 (Domain Services)
class DomainService(ABC):
    pass

class InventoryService(DomainService):
    @abstractmethod
    def update_stock(self, supply_id: int, quantity_change: int, transaction_type: TransactionType, user_id: int, notes: str = "") -> SupplyEntity:
        pass
    
    @abstractmethod
    def check_low_stock(self, supply_id: int) -> bool:
        pass
    
    @abstractmethod
    def is_available_for_reservation(self, supply_id: int, quantity: int, start_date: datetime, end_date: datetime) -> bool:
        pass

class ReservationService(DomainService):
    @abstractmethod
    def create_reservation(self, reservation: ReservationEntity) -> ReservationEntity:
        pass
    
    @abstractmethod
    def approve_reservation(self, reservation_id: int, approver_id: int) -> ReservationEntity:
        pass
    
    @abstractmethod
    def cancel_reservation(self, reservation_id: int, user_id: int) -> bool:
        pass

class AuthenticationService(DomainService):
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    def generate_token(self, user: UserEntity) -> str:
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[str]:
        pass

# 애플리케이션 계층 (Application Layer)

class UseCase(ABC):
    pass

class CreateSupplyUseCase(UseCase):
    def __init__(self, supply_repository: SupplyRepository, category_repository: SupplyCategoryRepository, inventory_service: InventoryService):
        self.supply_repository = supply_repository
        self.category_repository = category_repository
        self.inventory_service = inventory_service
    
    def execute(self, supply_data: dict, user_id: int) -> SupplyEntity:
        # 비즈니스 로직 검증
        if not self.category_repository.get_by_id(supply_data['category_id']):
            raise ValueError("Invalid category")
        
        if supply_data['quantity'] < 0:
            raise ValueError("Quantity cannot be negative")
        
        # 엔티티 생성
        supply = SupplyEntity(**supply_data)
        
        # 재고 상태 자동 설정
        if supply.quantity == 0:
            supply.status = SupplyStatus.OUT_OF_STOCK
        elif supply.quantity <= supply.min_quantity:
            supply.status = SupplyStatus.AVAILABLE
        else:
            supply.status = SupplyStatus.AVAILABLE
        
        # 저장
        return self.supply_repository.create(supply)

class GetSuppliesUseCase(UseCase):
    def __init__(self, supply_repository: SupplyRepository):
        self.supply_repository = supply_repository
    
    def execute(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, status: Optional[str] = None) -> List[SupplyEntity]:
        if category_id:
            return self.supply_repository.get_by_category(category_id)
        elif status:
            return self.supply_repository.get_by_status(SupplyStatus(status))
        else:
            return self.supply_repository.get_all(skip, limit)

class CreateReservationUseCase(UseCase):
    def __init__(self, reservation_repository: ReservationRepository, supply_repository: SupplyRepository, inventory_service: InventoryService):
        self.reservation_repository = reservation_repository
        self.supply_repository = supply_repository
        self.inventory_service = inventory_service
    
    def execute(self, reservation_data: dict, user_id: int) -> ReservationEntity:
        # 비품 존재 확인
        supply = self.supply_repository.get_by_id(reservation_data['supply_id'])
        if not supply:
            raise ValueError("Supply not found")
        
        # 재고 확인
        if not self.inventory_service.is_available_for_reservation(
            reservation_data['supply_id'], 
            reservation_data['quantity'],
            reservation_data['start_date'],
            reservation_data['end_date']
        ):
            raise ValueError("Supply not available for this period")
        
        # 예약 중복 확인
        overlapping = self.reservation_repository.get_overlapping_reservations(
            reservation_data['supply_id'],
            reservation_data['start_date'],
            reservation_data['end_date']
        )
        
        if overlapping:
            raise ValueError("Supply already reserved for this period")
        
        # 예약 생성
        reservation = ReservationEntity(**reservation_data, user_id=user_id)
        return self.reservation_repository.create(reservation)

class LoginUseCase(UseCase):
    def __init__(self, user_repository: UserRepository, auth_service: AuthenticationService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def execute(self, email: str, password: str) -> dict:
        user = self.auth_service.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid credentials")
        
        if not user.is_active:
            raise ValueError("User is inactive")
        
        token = self.auth_service.generate_token(user)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

# 애플리케이션 서비스 (Application Services)
class SupplyApplicationService:
    def __init__(self, create_supply_use_case: CreateSupplyUseCase, get_supplies_use_case: GetSuppliesUseCase):
        self.create_supply_use_case = create_supply_use_case
        self.get_supplies_use_case = get_supplies_use_case
    
    def create_supply(self, supply_data: dict, user_id: int) -> SupplyEntity:
        return self.create_supply_use_case.execute(supply_data, user_id)
    
    def get_supplies(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, status: Optional[str] = None) -> List[SupplyEntity]:
        return self.get_supplies_use_case.execute(skip, limit, category_id, status)

class AuthApplicationService:
    def __init__(self, login_use_case: LoginUseCase):
        self.login_use_case = login_use_case
    
    def login(self, email: str, password: str) -> dict:
        return self.login_use_case.execute(email, password)

class ReservationApplicationService:
    def __init__(self, create_reservation_use_case: CreateReservationUseCase):
        self.create_reservation_use_case = create_reservation_use_case
    
    def create_reservation(self, reservation_data: dict, user_id: int) -> ReservationEntity:
        return self.create_reservation_use_case.execute(reservation_data, user_id)
