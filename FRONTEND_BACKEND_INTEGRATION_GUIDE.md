# 🎨 프론트엔드-백엔드 연동 완벽 가이드

## 🎯 개요

Clean Architecture 기반 FastAPI 백엔드와 Lovable 생성 프론트엔드의 완벽한 연동 방법을 상세히 안내합니다.

---

## 🏗️ 아키텍처 개요

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Lovable     │    │  Clean Arch    │    │   SQLite       │
│  Frontend     │◄──►│   Backend       │◄──►|   Database     │
│  (React/Vue)  │    │   (FastAPI)     │    │                │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📋 연동 계층
1. **프론트엔드**: Lovable 생성 React/Vue 컴포넌트
2. **API 서비스**: 백엔드와의 통신 계층
3. **백엔드**: Clean Architecture FastAPI
4. **데이터베이스**: SQLite/PostgreSQL

---

## 🔧 API 연동 설정

### 1. **환경 변수 설정**

#### 프론트엔드 (`.env`)
```env
# API 기본 URL
VITE_API_URL=http://localhost:8000/api/v1

# 애플리케이션 이름
VITE_APP_NAME=비품 관리 시스템

# 개발 모드
VITE_DEV_MODE=true
```

#### 백엔드 (`.env`)
```env
# 데이터베이스 URL
DATABASE_URL=sqlite:///./supplies.db

# 보안 설정
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS 설정
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:80"]
```

### 2. **API 서비스 구현**

#### `frontend/src/services/api.ts`
```typescript
// API 서비스 - 백엔드와의 통신을 담당
const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
    username: string;
    role: string;
    department?: string;
  };
}

export interface Supply {
  id: number;
  name: string;
  description?: string;
  category_id: number;
  quantity: number;
  min_quantity: number;
  unit: string;
  location?: string;
  status: string;
  price?: number;
  created_at: string;
  updated_at?: string;
  category?: {
    id: number;
    name: string;
    description?: string;
  };
}

class ApiClient {
  private getAuthHeaders(token?: string): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
  }

  // 인증 관련
  async login(email: string, password: string): Promise<LoginResponse> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('로그인에 실패했습니다.');
    }

    return response.json();
  }

  async getCurrentUser(token: string): Promise<ApiResponse<any>> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getAuthHeaders(token),
    });

    return response.json();
  }

  // 비품 관리
  async getSupplies(token: string, params?: {
    skip?: number;
    limit?: number;
    category_id?: number;
    status?: string;
  }): Promise<ApiResponse<Supply[]>> {
    const url = new URL(`${API_BASE_URL}/supplies`);
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          url.searchParams.append(key, value.toString());
        }
      });
    }

    const response = await fetch(url.toString(), {
      headers: this.getAuthHeaders(token),
    });

    return response.json();
  }

  async createSupply(token: string, supplyData: Partial<Supply>): Promise<ApiResponse<Supply>> {
    const response = await fetch(`${API_BASE_URL}/supplies`, {
      method: 'POST',
      headers: this.getAuthHeaders(token),
      body: JSON.stringify(supplyData),
    });

    return response.json();
  }

  async updateSupply(token: string, id: number, supplyData: Partial<Supply>): Promise<ApiResponse<Supply>> {
    const response = await fetch(`${API_BASE_URL}/supplies/${id}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(token),
      body: JSON.stringify(supplyData),
    });

    return response.json();
  }

  async deleteSupply(token: string, id: number): Promise<ApiResponse<any>> {
    const response = await fetch(`${API_BASE_URL}/supplies/${id}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(token),
    });

    return response.json();
  }
}

export const apiClient = new ApiClient();
```

### 3. **인증 서비스 구현**

#### `frontend/src/services/auth.ts`
```typescript
// 인증 관련 서비스
import { apiClient, type LoginResponse } from './api';

export class AuthService {
  private static instance: AuthService;
  private token: string | null = null;
  private user: any = null;

  static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await apiClient.login(email, password);
      this.token = response.access_token;
      this.user = response.user;
      
      // 로컬 스토리지에 저장
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      return response;
    } catch (error) {
      throw new Error('로그인에 실패했습니다.');
    }
  }

  logout(): void {
    this.token = null;
    this.user = null;
    
    // 로컬 스토리지에서 제거
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }

  isAuthenticated(): boolean {
    return this.token !== null;
  }

  getToken(): string | null {
    return this.token || localStorage.getItem('access_token');
  }

  getUser(): any {
    if (this.user) {
      return this.user;
    }
    
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        this.user = JSON.parse(userStr);
        return this.user;
      } catch {
        return null;
      }
    }
    
    return null;
  }

  isAdmin(): boolean {
    const user = this.getUser();
    return user?.role === 'admin';
  }

  isManager(): boolean {
    const user = this.getUser();
    return user?.role === 'manager' || user?.role === 'admin';
  }

  // 초기화 (앱 시작 시 호출)
  initialize(): void {
    this.token = localStorage.getItem('access_token');
    this.user = null; // getUser()에서 자동 로드
  }
}

export const authService = AuthService.getInstance();
```

---

## 🎨 기본 화면 구성

### 1. **로그인 화면**

#### `frontend/src/pages/LoginPage.tsx`
```typescript
import React, { useState } from 'react';
import { authService } from '../services/auth';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authService.login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError('로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            비품 관리 시스템
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            로그인하여 시스템에 접속하세요
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                이메일
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="admin@company.com"
              />
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                비밀번호
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="•••••••••"
              />
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? '로그인 중...' : '로그인'}
            </button>
          </div>

          <div className="text-sm text-gray-600">
            <p>테스트 계정:</p>
            <ul className="mt-2 space-y-1">
              <li>관리자: admin@company.com / admin123</li>
              <li>매니저: manager@company.com / manager123</li>
              <li>사용자: user@company.com / user123</li>
            </ul>
          </div>
        </form>
      </div>
    </div>
  );
}
```

### 2. **대시보드 화면**

#### `frontend/src/pages/DashboardPage.tsx`
```typescript
import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { apiClient } from '../services/api';

export default function DashboardPage() {
  const { user, isAuthenticated, logout } = useAuth();
  const [supplies, setSupplies] = useState([]);
  const [lowStockAlerts, setLowStockAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      window.location.href = '/login';
      return;
    }

    const fetchData = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          // 비품 목록 조회
          const suppliesResponse = await apiClient.getSupplies(token);
          if (suppliesResponse.success) {
            setSupplies(suppliesResponse.data || []);
          }

          // 저재고 알림 조회
          const alertsResponse = await apiClient.getLowStockAlerts(token);
          if (alertsResponse.success) {
            setLowStockAlerts(alertsResponse.data || []);
          }
        }
      } catch (error) {
        console.error('데이터 조회 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [isAuthenticated]);

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">비품 관리 대시보드</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                환영합니다, {user?.username}님!
              </span>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 메인 콘텐츠 */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {/* 통계 카드 */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                    <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4M2 17l8 4 8-4m-8-4l8 4m-8-4l8 4" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        전체 비품
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {supplies.length}개
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            {/* 저재고 알림 */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-red-500 rounded-md p-3">
                    <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 2.502-3.162V7.667c0-1.495-.962-3.162-2.502-3.162H4.082c-1.54 0-2.502 1.667-2.502 3.162v4.171c0 1.495.962 3.162 2.502 3.162z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        저재고 알림
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {lowStockAlerts.length}개
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 비품 목록 */}
          <div className="mt-8">
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                  비품 목록
                </h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          이름
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          수량
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          상태
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          위치
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {supplies.map((supply) => (
                        <tr key={supply.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {supply.name}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {supply.quantity}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              supply.status === 'available' 
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}>
                              {supply.status === 'available' ? '사용 가능' : '사용 불가'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {supply.location || '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
```

### 3. **React Hook**

#### `frontend/src/hooks/useAuth.ts`
```typescript
import { useState, useEffect } from 'react';
import { authService } from '../services/auth';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 초기화
    authService.initialize();
    
    // 현재 상태 확인
    const authStatus = authService.isAuthenticated();
    const currentUser = authService.getUser();
    
    setIsAuthenticated(authStatus);
    setUser(currentUser);
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      await authService.login(email, password);
      setIsAuthenticated(true);
      setUser(authService.getUser());
      return true;
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setUser(null);
  };

  return {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    isAdmin: authService.isAdmin(),
    isManager: authService.isManager(),
  };
}
```

---

## 🚀 실행 방법

### 1. **개발 환경**
```bash
# 1. 백엔드 실행
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python simple_test.py
uvicorn main:app --reload --port 8000

# 2. 프론트엔드 실행
cd frontend
npm install
npm run dev
```

### 2. **Docker로 전체 시스템**
```bash
docker-compose up --build
```

### 3. **접속**
- 🎨 프론트엔드: http://localhost:3000
- ⚙️ 백엔드 API: http://localhost:8000
- 📚 API 문서: http://localhost:8000/docs

---

## 🔑 테스트 계정

| 역할 | 이메일 | 비밀번호 | 권한 |
|------|--------|----------|------|
| 👑 관리자 | admin@company.com | admin123 | 전체 권한 |
| 👨‍💼 매니저 | manager@company.com | manager123 | 비품 관리 |
| 👤 사용자 | user@company.com | user123 | 조회만 가능 |

---

## 📋 API 엔드포인트

### 🔐 인증
- `POST /api/v1/auth/login` - 로그인
- `GET /api/v1/auth/me` - 현재 사용자 정보

### 📦 비품 관리
- `GET /api/v1/supplies` - 비품 목록
- `POST /api/v1/supplies` - 비품 생성
- `PUT /api/v1/supplies/{id}` - 비품 수정
- `DELETE /api/v1/supplies/{id}` - 비품 삭제
- `GET /api/v1/supplies/low-stock/alerts` - 저재고 알림

---

## 🎯 주요 기능

### ✅ **구현된 기능**
- 🔐 **JWT 인증**: 토큰 기반 인증 시스템
- 📦 **비품 CRUD**: 생성, 조회, 수정, 삭제
- 📊 **대시보드**: 통계 및 현황
- 🔔 **저재고 알림**: 자동 알림 시스템
- 🎨 **반응형 UI**: 모바일 지원

### 🔄 **데이터 흐름**
1. 사용자 로그인 → JWT 토큰 발급
2. 토큰 저장 → API 요청 시 자동 포함
3. 백엔드 API → 데이터 처리 및 응답
4. 프론트엔드 → 데이터 표시 및 상태 관리

---

## 🎊 팁 및 모범 사례

### ✅ **코드 품질**
- TypeScript로 타입 안전성 확보
- 에러 핸들링 및 사용자 피드백
- 로딩 상태 및 비동기 처리
- 컴포넌트 분리 및 재사용성

### 🚀 **성능 최적화**
- API 요청 캐싱
- 불필요한 리렌더링 방지
- 이미지 및 정적 자원 최적화
- 코드 스플리팅 및 레이지 로딩

### 🔒 **보안**
- HTTPS 적용 (프로덕션)
- XSS 방지를 위한 입력 검증
- CSRF 토큰 사용
- 민감 정보 로컬 스토리지 관리

---

## 🎯 다음 단계

### 1. **기능 확장**
- 📅 예약 시스템 구현
- 📊 상세 분석 대시보드
- 🔔 실시간 알림 시스템
- 📱 모바일 앱 연동

### 2. **고급 기능**
- 🔄 실시간 데이터 동기화 (WebSocket)
- 📊 데이터 시각화 차트
- 🔍 고급 검색 및 필터링
- 📤 데이터 엑셀 내보내기

### 3. **운영**
- 🌐 프로덕션 배포
- 📊 모니터링 및 로깅
- 🔧 CI/CD 파이프라인
- 📱 사용자 분석 및 추적

---

## 🎉 결론

이 가이드를 통해 Lovable 프론트엔드와 Clean Architecture 백엔드의 완벽한 연동이 가능합니다. 모든 코드는 실제 프로젝트에서 바로 사용할 수 있도록 구현되었습니다.

**🎯 지금 바로 시작해보세요!**

```bash
git clone https://github.com/hnyun94/workflow-project.git
cd workflow-project
docker-compose up --build
```

**🌐 http://localhost:3000에서 완벽한 하이브리드 SaaS를 경험하세요!**
