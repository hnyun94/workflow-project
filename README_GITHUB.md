# 🚀 Lovable 연동을 위한 GitHub 저장소

## 📋 저장소 정보

- **GitHub**: https://github.com/hnyun94/workflow-project.git
- **프로젝트**: 하이브리드 SaaS 비품 관리 시스템
- **상태**: ✅ 백엔드 완료, Lovable 프론트엔드 연동 준비 완료

## 🎯 Lovable 연동 단계

### 1. Lovable 프로젝트 생성
Lovable에서 다음 프롬프트로 새 프로젝트 생성:

```
사내 비품 관리 시스템 대시보드를 만들어줘. 

주요 기능:
- 비품 목록 조회 (카테고리별 필터링)
- 재고 현황 시각화
- 비품 예약 기능
- 입출고 기록 조회
- 사용자 프로필 관리
- 관리자용 비품 등록/수정 기능

API 연동:
- 기본 URL: http://localhost:8000/api/v1
- 인증: JWT Bearer 토큰
- 주요 엔드포인트: /auth/login, /supplies, /reservations, /transactions

디자인 요구사항:
- 현대적이고 미니멀한 디자인
- 반응형 웹 (모바일 지원)
- 다크/라이트 모드 지원
- 실시간 재고 상태 표시
```

### 2. Lovable에서 Git으로 내보내기
1. Lovable 프로젝트에서 "Export" 버튼 클릭
2. "Export to Git" 선택
3. GitHub 저장소 연결: `https://github.com/hnyun94/workflow-project.git`
4. 새 브랜치 생성 (예: `frontend`)
5. 내보내기 완료

### 3. 프론트엔드 코드 확인
```bash
# Lovable이 내보낸 코드 확인
git checkout frontend
ls -la

# 메인 브랜치로 복귀
git checkout main
```

### 4. API 연동 코드 추가
Lovable이 내보낸 프론트엔드 코드에 API 연동 로직 추가:

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

## 🏗️ 프로젝트 구조

```
workflow-project/
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
├── docs/                   # API 문서 및 연동 가이드
├── frontend/               # Lovable에서 내보낸 프론트엔드 코드
├── docker-compose.yml      # 배포 설정
└── README_GITHUB.md        # 이 파일
```

## 🚀 빠른 시작

### 백엔드 실행
```bash
# 1. 저장소 클론
git clone https://github.com/hnyun94/workflow-project.git
cd workflow-project

# 2. 백엔드 설정
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. 데이터베이스 초기화
python simple_test.py

# 4. 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API 테스트
```bash
# 로그인
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@company.com&password=admin123"

# API 문서
open http://localhost:8000/docs
```

## 📚 API 문서

- **Swagger UI**: http://localhost:8000/docs
- **상세 문서**: [docs/api-documentation.md](docs/api-documentation.md)
- **Lovable 연동 가이드**: [docs/lovable-integration.md](docs/lovable-integration.md)

## 🔑 테스트 계정

| 역할 | 이메일 | 비밀번호 |
|------|--------|----------|
| 관리자 | admin@company.com | admin123 |
| 매니저 | manager@company.com | manager123 |
| 사용자 | user@company.com | user123 |

## 🎯 다음 단계

1. **Lovable에서 프론트엔드 생성** (위 프롬프트 사용)
2. **Git으로 내보내기** (이 저장소의 frontend 브랜치)
3. **API 연동 코드 추가** (연동 가이드 참조)
4. **전체 시스템 테스트**

## 🐛 문제 해결

### 백엔드 실행 문제
```bash
# 의존성 재설치
pip install -r requirements.txt

# 데이터베이스 재초기화
rm supplies.db
python simple_test.py
```

### API 연동 문제
- CORS 오류: 백엔드의 CORS 설정 확인
- 인증 오류: 토큰 저장 및 헤더 설정 확인
- 네트워크 오류: API URL 정확성 확인

## 📞 지원

- **API 문서**: http://localhost:8000/docs
- **이슈 리포트**: GitHub Issues
- **연동 가이드**: docs/lovable-integration.md

---

🎉 **이제 Lovable에서 프론트엔드를 생성하고 이 저장소와 연동할 준비가 완료되었습니다!**
