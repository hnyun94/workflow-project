# 비품 관리 시스템 API 문서

## 개요

이 API는 사내 비품 관리 시스템의 백엔드 기능을 제공합니다. FastAPI로 구현되었으며 JWT 인증을 사용합니다.

**기본 URL**: `http://localhost:8000/api/v1`

## 인증

모든 API 엔드포인트(인증 관련 제외)는 JWT Bearer 토큰이 필요합니다.

```http
Authorization: Bearer <your_jwt_token>
```

## 데이터 모델

### User (사용자)
```json
{
  "id": 1,
  "email": "user@company.com",
  "username": "홍길동",
  "department": "개발팀",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**역할 종류**:
- `admin`: 시스템 관리자 (전체 권한)
- `manager`: 부서 관리자 (비품 관리 권한)
- `user`: 일반 사용자 (조회 및 예약 권한)

### Supply (비품)
```json
{
  "id": 1,
  "name": "노트북",
  "description": "업무용 노트북",
  "category_id": 1,
  "quantity": 10,
  "min_quantity": 2,
  "unit": "대",
  "location": "A창고-1열",
  "status": "available",
  "price": 1500000.00,
  "created_at": "2024-01-01T00:00:00Z",
  "category": {
    "id": 1,
    "name": "전자기기"
  }
}
```

**상태 종류**:
- `available`: 사용 가능
- `out_of_stock`: 재고 없음
- `reserved`: 예약됨
- `maintenance`: 점검 중

### SupplyCategory (비품 카테고리)
```json
{
  "id": 1,
  "name": "전자기기",
  "description": "노트북, 모니터 등",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### SupplyTransaction (입출고 기록)
```json
{
  "id": 1,
  "supply_id": 1,
  "user_id": 1,
  "transaction_type": "in",
  "quantity": 5,
  "quantity_before": 5,
  "quantity_after": 10,
  "notes": "신규 입고",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**거래 종류**:
- `in`: 입고
- `out`: 출고
- `reserve`: 예약

### Reservation (예약)
```json
{
  "id": 1,
  "supply_id": 1,
  "user_id": 1,
  "quantity": 2,
  "start_date": "2024-01-01T09:00:00Z",
  "end_date": "2024-01-03T18:00:00Z",
  "purpose": "프로젝트 사용",
  "status": "pending",
  "approved_by": null,
  "notes": null,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**예약 상태**:
- `pending`: 대기 중
- `approved`: 승인됨
- `rejected`: 거절됨
- `completed`: 완료됨
- `cancelled`: 취소됨

## API 엔드포인트

### 1. 인증 (Authentication)

#### 회원가입
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@company.com",
  "username": "홍길동",
  "password": "password123",
  "department": "개발팀",
  "role": "user"
}
```

#### 로그인
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@company.com&password=password123
```

**응답**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 현재 사용자 정보
```http
GET /auth/me
Authorization: Bearer <token>
```

### 2. 비품 관리 (Supplies)

#### 비품 목록 조회
```http
GET /supplies?skip=0&limit=100&category_id=1&status=available
Authorization: Bearer <token>
```

**쿼리 파라미터**:
- `skip`: 건너뛸 레코드 수 (기본값: 0)
- `limit`: 최대 조회 수 (기본값: 100)
- `category_id`: 카테고리 ID 필터
- `status`: 상태 필터

#### 비품 상세 조회
```http
GET /supplies/{supply_id}
Authorization: Bearer <token>
```

#### 비품 등록 (관리자/매니저)
```http
POST /supplies
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "노트북",
  "description": "업무용 노트북",
  "category_id": 1,
  "quantity": 10,
  "min_quantity": 2,
  "unit": "대",
  "location": "A창고-1열",
  "price": 1500000.00
}
```

#### 비품 수정 (관리자/매니저)
```http
PUT /supplies/{supply_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 8,
  "location": "A창고-2열"
}
```

#### 비품 삭제 (관리자)
```http
DELETE /supplies/{supply_id}
Authorization: Bearer <token>
```

#### 재고 부족 알림
```http
GET /supplies/low-stock/alerts
Authorization: Bearer <token>
```

### 3. 카테고리 (Categories)

#### 카테고리 목록
```http
GET /categories
Authorization: Bearer <token>
```

#### 카테고리 생성 (관리자/매니저)
```http
POST /categories
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "전자기기",
  "description": "노트북, 모니터 등"
}
```

#### 카테고리 상세
```http
GET /categories/{category_id}
Authorization: Bearer <token>
```

### 4. 입출고 기록 (Transactions)

#### 거래 기록 조회
```http
GET /transactions?skip=0&limit=100&supply_id=1
Authorization: Bearer <token>
```

#### 입출고 처리
```http
POST /transactions
Authorization: Bearer <token>
Content-Type: application/json

{
  "supply_id": 1,
  "transaction_type": "in",
  "quantity": 5,
  "notes": "신규 입고"
}
```

### 5. 예약 (Reservations)

#### 예약 목록
```http
GET /reservations?skip=0&limit=100&status=pending
Authorization: Bearer <token>
```

**권한**: 
- 일반 사용자: 자신의 예약만 조회
- 관리자/매니저: 전체 예약 조회

#### 예약 생성
```http
POST /reservations
Authorization: Bearer <token>
Content-Type: application/json

{
  "supply_id": 1,
  "quantity": 2,
  "start_date": "2024-01-01T09:00:00Z",
  "end_date": "2024-01-03T18:00:00Z",
  "purpose": "프로젝트 사용"
}
```

#### 예약 상세
```http
GET /reservations/{reservation_id}
Authorization: Bearer <token>
```

#### 예약 수정/승인
```http
PUT /reservations/{reservation_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "approved",
  "notes": "승인 완료"
}
```

#### 예약 취소
```http
DELETE /reservations/{reservation_id}
Authorization: Bearer <token>
```

### 6. 사용자 관리 (Users)

#### 사용자 목록 (관리자/매니저)
```http
GET /users
Authorization: Bearer <token>
```

#### 사용자 정보
```http
GET /users/{user_id}
Authorization: Bearer <token>
```

#### 사용자 정보 수정
```http
PUT /users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "이름변경",
  "department": "새부서"
}
```

## 에러 응답

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email address",
      "type": "value_error"
    }
  ]
}
```

## Swagger UI

백엔드 서버 실행 후 다음 URL에서 인터랙티브 API 문서를 확인할 수 있습니다:

`http://localhost:8000/docs`

## 테스트용 데이터

### 초기 관리자 계정
```json
{
  "email": "admin@company.com",
  "password": "admin123",
  "role": "admin"
}
```

### 샘플 카테고리
```json
[
  {"name": "전자기기", "description": "노트북, 모니터 등"},
  {"name": "사무용품", "description": "펜, 노트 등"},
  {"name": "가구", "description": "책상, 의자 등"}
]
```

### 샘플 비품
```json
[
  {
    "name": "노트북",
    "category_id": 1,
    "quantity": 10,
    "min_quantity": 2,
    "unit": "대",
    "location": "A창고-1열"
  },
  {
    "name": "모니터",
    "category_id": 1,
    "quantity": 15,
    "min_quantity": 3,
    "unit": "대",
    "location": "A창고-2열"
  }
]
```

## 개발 팁

1. **테스트**: Postman이나 Swagger UI를 사용하여 API 테스트
2. **디버깅**: 백엔드 로그에서 상세 오류 정보 확인
3. **CORS**: 프론트엔드 도메인이 CORS 허용 목록에 있는지 확인
4. **인증**: 토큰 만료 시 자동으로 재로그인 처리 구현
