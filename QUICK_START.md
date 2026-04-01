# 빠른 시작 가이드

## 5분 만에 비품 관리 시스템 실행하기

### 1. 사전 요구사항
- Docker 및 Docker Compose 설치
- Git

### 2. 프로젝트 클론 및 실행
```bash
# 프로젝트 클론
git clone <repository-url>
cd project3

# Docker Compose로 전체 시스템 실행
docker-compose up --build

# 백그라운드 실행 (선택사항)
docker-compose up -d --build
```

### 3. 시스템 접속
- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

### 4. 초기 관리자 계정 생성
API 문서에서 `/auth/register` 엔드포인트를 사용하여 관리자 계정을 생성하세요:

```json
{
  "email": "admin@company.com",
  "username": "관리자",
  "password": "admin123",
  "department": "IT팀",
  "role": "admin"
}
```

### 5. 기본 데이터 확인
시스템에는 이미 샘플 카테고리와 비품 데이터가 포함되어 있습니다.

---

## Lovable 프론트엔드 연동

### 1. Lovable 프로젝트 생성
다음 프롬프트로 Lovable 프로젝트를 생성하세요:

```
사내 비품 관리 시스템 대시보드를 만들어줘. 
주요 기능:
- 비품 목록 조회 (카테고리별 필터링)
- 재고 현황 시각화
- 비품 예약 기능
- 입출고 기록 조회
- 사용자 프로필 관리
- 관리자용 비품 등록/수정 기능

디자인 요구사항:
- 현대적이고 미니멀한 디자인
- 반응형 웹 (모바일 지원)
- 다크/라이트 모드 지원
- 실시간 재고 상태 표시

API 연동:
- 기본 URL: http://localhost:8000/api/v1
- 인증: JWT Bearer 토큰
- 주요 엔드포인트: /auth/login, /supplies, /reservations, /transactions
```

### 2. API 연동 코드
Lovable 프로젝트에 다음 코드를 추가하세요:

```javascript
// API 설정
const API_BASE_URL = 'http://localhost:8000/api/v1';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

// 로그인 함수
const login = async (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  if (response.ok) {
    localStorage.setItem('access_token', data.access_token);
    return true;
  }
  return false;
};
```

### 3. Lovable에서 Git으로 내보내기
1. Lovable 프로젝트에서 "Export" → "Export to Git"
2. GitHub 리포지토리 연결
3. 내보내기 완료 후 코드 클론

### 4. 프론트엔드 실행
```bash
cd your-lovable-project
npm install
npm start
```

---

## 개발 환경 설정

### 백엔드만 실행 (로컬 개발)
```bash
cd backend

# 가상환경 설정
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 데이터베이스만 실행
```bash
# PostgreSQL 실행
docker run --name supplies_db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=supplies_db -p 5432:5432 -d postgres:15

# 초기 데이터 삽입
psql -h localhost -U postgres -d supplies_db -f init.sql
```

---

## 주요 기능 테스트

### 1. 인증 테스트
```bash
# 로그인
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@company.com&password=admin123"
```

### 2. 비품 목록 조회
```bash
# 토큰을 변수에 저장
TOKEN="your_jwt_token_here"

# 비품 목록 조회
curl -X GET "http://localhost:8000/api/v1/supplies" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. 비품 등록
```bash
curl -X POST "http://localhost:8000/api/v1/supplies" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "새 비품",
    "description": "테스트용 비품",
    "category_id": 1,
    "quantity": 10,
    "min_quantity": 2,
    "unit": "개",
    "location": "테스트 창고"
  }'
```

---

## 문제 해결

### 1. 포트 충돌
```bash
# 사용 중인 포트 확인
lsof -i :8000
lsof -i :3000
lsof -i :5432

# 프로세스 종료
kill -9 <PID>
```

### 2. Docker 문제
```bash
# 모든 컨테이너 중지
docker-compose down

# 이미지 재빌드
docker-compose up --build --force-recreate

# 볼륨 초기화
docker-compose down -v
docker-compose up --build
```

### 3. 데이터베이스 연결 문제
```bash
# 데이터베이스 컨테이너 로그 확인
docker-compose logs postgres

# 데이터베이스 접속 테스트
docker exec -it supplies_db psql -U postgres -d supplies_db
```

---

## 다음 단계

1. **Lovable 프론트엔드 개발**: `docs/lovable-integration.md` 참조
2. **API 문서 확인**: `docs/api-documentation.md` 참조
3. **프로덕션 배포**: `DEPLOYMENT.md` 참조
4. **기능 확장**: 새로운 기능 추가 및 커스터마이징

---

## 지원

- **API 문서**: http://localhost:8000/docs
- **프로젝트 README**: `README.md`
- **배포 가이드**: `DEPLOYMENT.md`
- **Lovable 연동 가이드**: `docs/lovable-integration.md`

이제 하이브리드 SaaS 비품 관리 시스템을 사용할 준비가 완료되었습니다!
