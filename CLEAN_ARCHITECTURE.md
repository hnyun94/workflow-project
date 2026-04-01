# Clean Architecture 리팩토링 가이드

## 🏗️ Clean Architecture 구조

프로젝트를 Clean Architecture 패턴으로 리팩토링하여 유지보수성과 테스트 용이성을 향상시켰습니다.

### 📁 새로운 구조

```
backend/app/
├── domain/                     # 도메인 계층 (가장 내부)
│   ├── entities/              # 도메인 엔티티
│   │   ├── user.py
│   │   ├── supply.py
│   │   ├── reservation.py
│   │   └── transaction.py
│   ├── enums/                 # 도메인 열거형
│   │   └── common.py
│   ├── repositories/          # 리포지토리 인터페이스
│   │   ├── base.py
│   │   ├── user_repository.py
│   │   ├── supply_repository.py
│   │   └── reservation_repository.py
│   └── services/              # 도메인 서비스
│       ├── inventory_service.py
│       ├── reservation_service.py
│       └── auth_service.py
├── application/               # 애플리케이션 계층
│   ├── use_cases/            # 유스케이스
│   │   ├── base.py
│   │   └── supply_use_cases.py
│   └── dto/                   # 데이터 전송 객체
│       └── supply_dto.py
├── infrastructure/            # 인프라스트럭처 계층
│   ├── repositories/          # 리포지토리 구현
│   │   └── sqlalchemy_supply_repository.py
│   └── services/              # 인프라 서비스
│       └── sqlalchemy_inventory_service.py
├── presentation/             # 프레젠테이션 계층 (가장 외부)
│   ├── controllers/          # API 컨트롤러
│   │   └── supply_controller.py
│   └── di_container.py       # 의존성 주입 컨테이너
└── core/                      # 공통 (외부)
    ├── config.py
    ├── database.py
    └── security.py
```

## 🎯 Clean Architecture 원칙

### 1. 의존성 규칙
- **내부 계층은 외부 계층에 대해 알지 못함**
- **의존성은 항상 바깥에서 안쪽으로 향함**
- 도메인 계층은 다른 모든 계층에 대해 독립적

### 2. 계층별 책임

#### 도메인 계층 (Domain Layer)
- **엔티티**: 비즈니스 규칙과 데이터를 포함
- **값 객체**: 불변적인 비즈니스 값
- **도메인 서비스**: 복잡한 비즈니스 로직
- **리포지토리 인터페이스**: 데이터 접근 추상화

```python
# 예시: 도메인 엔티티
@dataclass
class Supply:
    id: Optional[int] = None
    name: str = ""
    quantity: int = 0
    status: SupplyStatus = SupplyStatus.AVAILABLE
    
    def add_stock(self, quantity: int) -> 'Supply':
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.quantity += quantity
        self._update_status()
        return self
```

#### 애플리케이션 계층 (Application Layer)
- **유스케이스**: 특정 비즈니스 시나리오 구현
- **DTO**: 계층 간 데이터 전송
- **애플리케이션 서비스**: 유스케이스 조합

```python
# 예시: 유스케이스
class CreateSupplyUseCase(UseCase):
    def execute(self, request: CreateSupplyRequest, user_id: int) -> UseCaseResponse:
        # 비즈니스 로직 검증
        if not self.category_repository.get_by_id(request.category_id):
            return ErrorResponse("Invalid category")
        
        # 엔티티 생성 및 저장
        supply = Supply(**request.__dict__)
        return SuccessResponse(self.supply_repository.create(supply))
```

#### 인프라스트럭처 계층 (Infrastructure Layer)
- **리포지토리 구현**: 데이터베이스 접근
- **외부 서비스**: API 클라이언트, 메시지 큐 등
- **프레임워크 특정 코드**: SQLAlchemy, FastAPI 등

```python
# 예시: 리포지토리 구현
class SQLAlchemySupplyRepository(SupplyRepository):
    def create(self, entity: Supply) -> Supply:
        model = self._entity_to_model(entity)
        self.db.add(model)
        self.db.commit()
        return self._model_to_entity(model)
```

#### 프레젠테이션 계층 (Presentation Layer)
- **API 컨트롤러**: HTTP 요청/응답 처리
- **미들웨어**: 인증, 로깅 등
- **의존성 주입**: 서비스 연결

```python
# 예시: 컨트롤러
@router.post("/", response_model=dict)
async def create_supply(
    supply_data: dict,
    use_case: CreateSupplyUseCase = Depends(get_create_supply_use_case)
):
    request = CreateSupplyRequest(**supply_data)
    response = use_case.execute(request, current_user.id)
    return response.data
```

## 🔄 리팩토링 전후 비교

### 이전 구조 (3-Layer Architecture)
```
models/          # 데이터 모델 + 비즈니스 로직
schemas/         # API 스키마
services/        # 비즈니스 로직
api/            # API 컨트롤러
```

### 새로운 구조 (Clean Architecture)
```
domain/         # 순수 비즈니스 로직
application/    # 유스케이스 조합
infrastructure/ # 기술적 구현
presentation/   # 외부 인터페이스
```

## 🚀 장점

### 1. 테스트 용이성
- 도메인 로직을 독립적으로 테스트 가능
- 모의 객체(Mock) 사용 용이
- 단위 테스트 작성 간소

### 2. 유지보수성
- 비즈니스 로직 변경 시 다른 계층 영향 최소화
- 기술 스택 교체 용이 (SQLAlchemy → 다른 ORM)
- 코드 재사용성 증가

### 3. 확장성
- 새로운 유스케이스 추가 용이
- 새로운 인프라 구현 추가 용이
- 마이크로서비스로 분리 용이

## 🛠️ 사용 방법

### 1. 새로운 엔티티 추가
```python
# domain/entities/new_entity.py
@dataclass
class NewEntity:
    # 도메인 규칙과 비즈니스 로직
    pass
```

### 2. 새로운 유스케이스 추가
```python
# application/use_cases/new_use_case.py
class NewUseCase(UseCase):
    def execute(self, request: NewRequest) -> UseCaseResponse:
        # 유스케이스 로직
        pass
```

### 3. 새로운 컨트롤러 추가
```python
# presentation/controllers/new_controller.py
@router.post("/")
async def new_endpoint(
    request: NewRequest,
    use_case: NewUseCase = Depends(get_new_use_case)
):
    response = use_case.execute(request)
    return response.data
```

## 📋 마이그레이션 가이드

### 기존 코드를 Clean Architecture로迁移

1. **도메인 엔티티 추출**
   ```python
   # models/supply.py → domain/entities/supply.py
   # 비즈니스 로직만 남기고 기술적 의존성 제거
   ```

2. **리포지토리 인터페이스 정의**
   ```python
   # domain/repositories/supply_repository.py
   # 데이터 접근 로직을 인터페이스로 추상화
   ```

3. **유스케이스 재구성**
   ```python
   # services/supply_service.py → application/use_cases/supply_use_cases.py
   # 비즈니스 시나리오별로 유스케이스 분리
   ```

4. **컨트롤러 수정**
   ```python
   # api/v1/endpoints/supplies.py → presentation/controllers/supply_controller.py
   # 유스케이스 호출 방식으로 변경
   ```

## 🧪 테스트 전략

### 도메인 계층 테스트
```python
def test_supply_add_stock():
    supply = Supply(name="Test", quantity=10)
    supply.add_stock(5)
    assert supply.quantity == 15
```

### 유스케이스 테스트
```python
def test_create_supply_use_case():
    # 모의 리포지토리 사용
    mock_repo = Mock(spec=SupplyRepository)
    use_case = CreateSupplyUseCase(mock_repo, ...)
    
    response = use_case.execute(request, user_id)
    assert response.success
```

## 🎯 다음 단계

1. **나머지 엔티티 리팩토링**: User, Reservation, Transaction
2. **통합 테스트 추가**: 계층 간 연동 테스트
3. **의존성 주입 개선**: 더 정교한 DI 컨테이너
4. **성능 최적화**: 캐싱, 배치 처리 등

---

Clean Architecture를 통해 코드의 품질과 유지보수성이 크게 향상되었습니다! 🎉
