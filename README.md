# 프로젝트 3: 하이브리드 SaaS 비품 관리 시스템

Lovable (Frontend) + FastAPI (Backend)로 구현하는 비품 관리 시스템

## 프로젝트 구조

```
project3/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 라우트
│   │   ├── core/           # 설정 및 보안
│   │   ├── models/         # 데이터 모델
│   │   ├── schemas/        # Pydantic 스키마
│   │   └── services/       # 비즈니스 로직
│   ├── alembic/            # 데이터베이스 마이그레이션
│   ├── requirements.txt    # Python 의존성
│   └── main.py            # 애플리케이션 진입점
├── frontend/               # Lovable에서 내보낸 프론트엔드 코드
├── docs/                   # API 문서 및 통합 가이드
└── docker-compose.yml      # 배포 설정
```

## 주요 기능

- 🔐 사용자 인증 및 권한 관리
- 📦 비품 재고 관리 (CRUD)
- 📊 재고 현황 대시보드
- 🔄 비품 입/출고 기록
- 📑 비품 예약 및 대여 시스템
- 🔔 재고 부족 알림

## 기술 스택

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL
- SQLAlchemy + Alembic
- JWT Authentication
- Pydantic

**Frontend:**
- Lovable (AI 기반 UI 생성)
- React/Next.js (Lovable 내보내기)
- TailwindCSS

## 시작하기

### 백엔드 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 데이터베이스 설정
```bash
alembic upgrade head
```

## API 문서

백엔드 실행 후 `http://localhost:8000/docs`에서 Swagger UI 확인

## Lovable 연동

`docs/lovable-integration.md` 참조
