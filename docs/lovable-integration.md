# Lovable 프론트엔드 연동 가이드

이 가이드는 Lovable로 생성한 프론트엔드를 FastAPI 백엔드와 연동하는 방법을 설명합니다.

## 1. Lovable 프로젝트 설정

### 1.1 새 프로젝트 생성
```
프롬프트 예시:
"사내 비품 관리 시스템 대시보드를 만들어줘. 
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
- 실시간 재고 상태 표시"
```

### 1.2 API 연동을 위한 설정
Lovable 프로젝트에서 다음 API 엔드포인트들을 사용하도록 설정:

```javascript
// API 기본 설정
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// 인증 헤더 설정
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};
```

## 2. 백엔드 API 엔드포인트

### 2.1 인증 API
- `POST /auth/register` - 회원가입
- `POST /auth/login` - 로그인
- `GET /auth/me` - 현재 사용자 정보

### 2.2 비품 관리 API
- `GET /supplies` - 비품 목록 조회
- `GET /supplies/{id}` - 비품 상세 정보
- `POST /supplies` - 비품 등록 (관리자/매니저)
- `PUT /supplies/{id}` - 비품 수정 (관리자/매니저)
- `DELETE /supplies/{id}` - 비품 삭제 (관리자)
- `GET /supplies/low-stock/alerts` - 재고 부족 알림

### 2.3 카테고리 API
- `GET /categories` - 카테고리 목록
- `POST /categories` - 카테고리 생성 (관리자/매니저)

### 2.4 거래 기록 API
- `GET /transactions` - 입출고 기록
- `POST /transactions` - 입출고 처리

### 2.5 예약 API
- `GET /reservations` - 예약 목록
- `POST /reservations` - 예약 생성
- `GET /reservations/{id}` - 예약 상세
- `PUT /reservations/{id}` - 예약 수정/승인
- `DELETE /reservations/{id}` - 예약 취소

## 3. Lovable에서의 API 연동 코드 예시

### 3.1 인증 컴포넌트
```javascript
// 로그인 컴포넌트
const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
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
        // 로그인 성공 후 리디렉션
        window.location.href = '/dashboard';
      } else {
        alert('로그인 실패: ' + data.detail);
      }
    } catch (error) {
      alert('로그인 중 오류 발생: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="이메일"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="비밀번호"
        required
      />
      <button type="submit">로그인</button>
    </form>
  );
};
```

### 3.2 비품 목록 컴포넌트
```javascript
// 비품 목록 컴포넌트
const SuppliesList = () => {
  const [supplies, setSupplies] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    fetchSupplies();
    fetchCategories();
  }, [selectedCategory]);

  const fetchSupplies = async () => {
    try {
      const url = selectedCategory 
        ? `${API_BASE_URL}/supplies?category_id=${selectedCategory}`
        : `${API_BASE_URL}/supplies`;
      
      const response = await fetch(url, {
        headers: getAuthHeaders()
      });

      if (response.ok) {
        const data = await response.json();
        setSupplies(data);
      }
    } catch (error) {
      console.error('비품 목록 조회 실패:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/categories`, {
        headers: getAuthHeaders()
      });

      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (error) {
      console.error('카테고리 조회 실패:', error);
    }
  };

  return (
    <div>
      <h2>비품 목록</h2>
      
      {/* 카테고리 필터 */}
      <select 
        value={selectedCategory} 
        onChange={(e) => setSelectedCategory(e.target.value)}
      >
        <option value="">전체 카테고리</option>
        {categories.map(cat => (
          <option key={cat.id} value={cat.id}>{cat.name}</option>
        ))}
      </select>

      {/* 비품 목록 */}
      <div className="supplies-grid">
        {supplies.map(supply => (
          <div key={supply.id} className="supply-card">
            <h3>{supply.name}</h3>
            <p>{supply.description}</p>
            <p>카테고리: {supply.category?.name}</p>
            <p>수량: {supply.quantity} {supply.unit}</p>
            <p>위치: {supply.location}</p>
            <p>상태: {supply.status}</p>
            
            {/* 재고 상태에 따른 스타일 */}
            {supply.quantity <= supply.min_quantity && (
              <div className="low-stock-warning">
                ⚠️ 재고 부족
              </div>
            )}
            
            <button onClick={() => handleReservation(supply.id)}>
              예약하기
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 3.3 예약 컴포넌트
```javascript
// 비품 예약 컴포넌트
const ReservationForm = ({ supplyId, onClose }) => {
  const [quantity, setQuantity] = useState(1);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [purpose, setPurpose] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API_BASE_URL}/reservations`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          supply_id: supplyId,
          quantity,
          start_date: startDate,
          end_date: endDate,
          purpose
        })
      });

      if (response.ok) {
        alert('예약이 신청되었습니다.');
        onClose();
      } else {
        const error = await response.json();
        alert('예약 실패: ' + error.detail);
      }
    } catch (error) {
      alert('예약 중 오류 발생: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>비품 예약</h3>
      
      <div>
        <label>수량:</label>
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(parseInt(e.target.value))}
          min="1"
          required
        />
      </div>

      <div>
        <label>시작일:</label>
        <input
          type="datetime-local"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          required
        />
      </div>

      <div>
        <label>종료일:</label>
        <input
          type="datetime-local"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          required
        />
      </div>

      <div>
        <label>사용 목적:</label>
        <textarea
          value={purpose}
          onChange={(e) => setPurpose(e.target.value)}
          placeholder="사용 목적을 입력하세요"
        />
      </div>

      <button type="submit">예약 신청</button>
      <button type="button" onClick={onClose}>취소</button>
    </form>
  );
};
```

## 4. Lovable에서 Git으로 내보내기

### 4.1 내보내기 단계
1. Lovable 프로젝트에서 "Export" 버튼 클릭
2. "Export to Git" 선택
3. GitHub 리포지토리 연결 또는 새 리포지토리 생성
4. 내보내기 완료 후 코드 확인

### 4.2 내보낸 후 설정
```bash
# 클론한 프로젝트에서
cd your-lovable-project

# 환경 변수 설정
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env

# 의존성 설치
npm install

# 개발 서버 시작
npm start
```

## 5. 테스트 및 배포

### 5.1 로컬 테스트
1. 백엔드 서버 실행: `uvicorn main:app --reload`
2. 프론트엔드 서버 실행: `npm start`
3. 브라우저에서 `http://localhost:3000` 접속

### 5.2 배포 설정
```dockerfile
# Dockerfile for frontend
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 6. 주의사항

### 6.1 CORS 설정
백엔드의 `main.py`에서 CORS 설정을 확인하세요:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6.2 인증 처리
- JWT 토큰을 localStorage에 저장
- API 호출 시마다 Authorization 헤더에 토큰 포함
- 토큰 만료 시 자동 리프레시 또는 재로그인

### 6.3 에러 처리
- API 응답 상태 코드 확인
- 사용자 친화적인 에러 메시지 표시
- 네트워크 오류 시 재시도 로직

이 가이드를 따라 Lovable로 생성한 프론트엔드를 FastAPI 백엔드와 성공적으로 연동할 수 있습니다.
