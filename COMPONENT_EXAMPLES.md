# 🎨 프론트엔드 컴포넌트 예제 모음

## 🎯 개요

Lovable 생성 프론트엔드와 Clean Architecture 백엔드 연동을 위한 실용적인 컴포넌트 예제들을 제공합니다.

---

## 🏗️ 기본 컴포넌트 구조

### 1. **레이아웃 컴포넌트**

#### `frontend/src/components/Layout.tsx`
```typescript
import React from 'react';
import { useAuth } from '../hooks/useAuth';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const { user, isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) {
    return <div>{children}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 사이드바 */}
      <aside className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg">
        <div className="flex flex-col h-full">
          {/* 로고 */}
          <div className="flex items-center h-16 px-6 bg-indigo-600">
            <h1 className="text-white text-lg font-semibold">비품 관리</h1>
          </div>
          
          {/* 네비게이션 */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            <a
              href="/dashboard"
              className="bg-gray-100 text-gray-700 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
            >
              <svg className="text-gray-500 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3a1 1 0 001-1V10M7 7l3-3 3 3" />
              </svg>
              대시보드
            </a>
            
            <a
              href="/supplies"
              className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
            >
              <svg className="text-gray-400 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4M2 17l8 4 8-4m-8-4l8 4m-8-4l8 4" />
              </svg>
              비품 관리
            </a>
            
            {user?.role === 'admin' && (
              <a
                href="/users"
                className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
              >
                <svg className="text-gray-400 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 016-7v-4a6 6 0 00-6-7H3m7 10a4 4 0 008 0m-8-4a4 4 0 118 0m0 0a4 4 0 018 0" />
                </svg>
                사용자 관리
              </a>
            )}
          </nav>
          
          {/* 사용자 정보 */}
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0 h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center">
                <span className="text-white font-medium">
                  {user?.username?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-700">{user?.username}</p>
                <p className="text-xs font-medium text-gray-500">{user?.email}</p>
              </div>
            </div>
            <button
              onClick={logout}
              className="mt-3 w-full flex justify-center bg-red-600 px-3 py-2 text-sm font-medium text-white rounded-md hover:bg-red-700"
            >
              로그아웃
            </button>
          </div>
        </div>
      </aside>

      {/* 메인 콘텐츠 */}
      <div className="pl-64">
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}
```

### 2. **비품 카드 컴포넌트**

#### `frontend/src/components/SupplyCard.tsx`
```typescript
import React from 'react';
import { Supply } from '../services/api';

interface SupplyCardProps {
  supply: Supply;
  onEdit?: (supply: Supply) => void;
  onDelete?: (supply: Supply) => void;
  onView?: (supply: Supply) => void;
}

export default function SupplyCard({ supply, onEdit, onDelete, onView }: SupplyCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return 'bg-green-100 text-green-800';
      case 'low_stock':
        return 'bg-yellow-100 text-yellow-800';
      case 'out_of_stock':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'available':
        return '사용 가능';
      case 'low_stock':
        return '재고 부족';
      case 'out_of_stock':
        return '품절';
      default:
        return '알 수 없음';
    }
  };

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <h3 className="text-lg font-medium text-gray-900">{supply.name}</h3>
            {supply.description && (
              <p className="mt-1 text-sm text-gray-500">{supply.description}</p>
            )}
          </div>
          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(supply.status)}`}>
            {getStatusText(supply.status)}
          </span>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-gray-500">수량</p>
            <p className="mt-1 text-lg font-semibold text-gray-900">{supply.quantity}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">최소 수량</p>
            <p className="mt-1 text-lg font-semibold text-gray-900">{supply.min_quantity}</p>
          </div>
        </div>

        {supply.location && (
          <div className="mt-4">
            <p className="text-sm font-medium text-gray-500">위치</p>
            <p className="mt-1 text-sm text-gray-900">{supply.location}</p>
          </div>
        )}

        {supply.category && (
          <div className="mt-4">
            <p className="text-sm font-medium text-gray-500">카테고리</p>
            <p className="mt-1 text-sm text-gray-900">{supply.category.name}</p>
          </div>
        )}

        <div className="mt-6 flex justify-between">
          <div className="text-sm text-gray-500">
            생성일: {new Date(supply.created_at).toLocaleDateString()}
          </div>
          
          <div className="flex space-x-2">
            {onView && (
              <button
                onClick={() => onView(supply)}
                className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                <svg className="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                상세
              </button>
            )}
            
            {onEdit && (
              <button
                onClick={() => onEdit(supply)}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                <svg className="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 00-.586-1.414l-3-3a2 2 0 00-1.414 0l-3 3a2 2 0 001.414.586L18 9a2 2 0 002 2v-5a2 2 0 00-2-2z" />
                </svg>
                수정
              </button>
            )}
            
            {onDelete && (
              <button
                onClick={() => onDelete(supply)}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
              >
                <svg className="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m0 0l3-3m-3 3l-3-3m12-3l-3 3" />
                </svg>
                삭제
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
```

### 3. **비품 목록 컴포넌트**

#### `frontend/src/components/SupplyList.tsx`
```typescript
import React, { useState, useEffect } from 'react';
import { Supply } from '../services/api';
import SupplyCard from './SupplyCard';

interface SupplyListProps {
  onEdit?: (supply: Supply) => void;
  onDelete?: (supply: Supply) => void;
  onView?: (supply: Supply) => void;
}

export default function SupplyList({ onEdit, onDelete, onView }: SupplyListProps) {
  const [supplies, setSupplies] = useState<Supply[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSupplies = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/supplies`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setSupplies(data.data || []);
          } else {
            setError('비품 목록을 불러오는데 실패했습니다.');
          }
        }
      } catch (err) {
        setError('네트워크 오류가 발생했습니다.');
      } finally {
        setLoading(false);
      }
    };

    fetchSupplies();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg">로딩 중...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  if (supplies.length === 0) {
    return (
      <div className="text-center py-12">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414-2.414a1 1 0 00-.707 0l-2.414 2.414a1 1 0 00.293.707L16.586 13H18a2 2 0 002 2z" />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">등록된 비품이 없습니다</h3>
        <p className="mt-1 text-sm text-gray-500">첫 번째 비품을 등록해보세요.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {supplies.map((supply) => (
        <SupplyCard
          key={supply.id}
          supply={supply}
          onEdit={onEdit}
          onDelete={onDelete}
          onView={onView}
        />
      ))}
    </div>
  );
}
```

### 4. **비품 생성/수정 폼**

#### `frontend/src/components/SupplyForm.tsx`
```typescript
import React, { useState, useEffect } from 'react';
import { Supply } from '../services/api';

interface SupplyFormProps {
  supply?: Supply;
  onSubmit: (supplyData: Partial<Supply>) => void;
  onCancel: () => void;
  loading?: boolean;
}

export default function SupplyForm({ supply, onSubmit, onCancel, loading = false }: SupplyFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    quantity: 0,
    min_quantity: 1,
    unit: '개',
    location: '',
    category_id: 1,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (supply) {
      setFormData({
        name: supply.name,
        description: supply.description || '',
        quantity: supply.quantity,
        min_quantity: supply.min_quantity,
        unit: supply.unit,
        location: supply.location || '',
        category_id: supply.category_id,
      });
    }
  }, [supply]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'quantity' || name === 'min_quantity' ? Number(value) : value,
    }));
    
    // 에러 초기화
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = '비품 이름을 입력해주세요.';
    }

    if (formData.quantity <= 0) {
      newErrors.quantity = '수량은 0보다 커야 합니다.';
    }

    if (formData.min_quantity < 0) {
      newErrors.min_quantity = '최소 수량은 0 이상이어야 합니다.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
          {supply ? '비품 수정' : '비품 등록'}
        </h3>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                비품 이름 *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={`mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                  errors.name ? 'border-red-500' : ''
                }`}
                placeholder="예: A4 용지"
              />
              {errors.name && (
                <p className="mt-2 text-sm text-red-600">{errors.name}</p>
              )}
            </div>

            <div>
              <label htmlFor="quantity" className="block text-sm font-medium text-gray-700">
                수량 *
              </label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                min="0"
                className={`mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                  errors.quantity ? 'border-red-500' : ''
                }`}
              />
              {errors.quantity && (
                <p className="mt-2 text-sm text-red-600">{errors.quantity}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label htmlFor="min_quantity" className="block text-sm font-medium text-gray-700">
                최소 수량 *
              </label>
              <input
                type="number"
                id="min_quantity"
                name="min_quantity"
                value={formData.min_quantity}
                onChange={handleChange}
                min="0"
                className={`mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                  errors.min_quantity ? 'border-red-500' : ''
                }`}
              />
              {errors.min_quantity && (
                <p className="mt-2 text-sm text-red-600">{errors.min_quantity}</p>
              )}
            </div>

            <div>
              <label htmlFor="unit" className="block text-sm font-medium text-gray-700">
                단위 *
              </label>
              <input
                type="text"
                id="unit"
                name="unit"
                value={formData.unit}
                onChange={handleChange}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="예: 개, 박스, 병"
              />
            </div>
          </div>

          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700">
              위치
            </label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="예: 1층 창고"
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              설명
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="비품에 대한 상세 설명"
            />
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onCancel}
              className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              취소
            </button>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? '처리 중...' : (supply ? '수정' : '등록')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

---

## 🎨 스타일링 가이드

### 1. **Tailwind CSS 설정**

#### `frontend/src/index.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* 커스텀 컴포넌트 스타일 */
.btn-primary {
  @apply bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200;
}

.btn-secondary {
  @apply bg-white hover:bg-gray-50 text-gray-700 font-medium py-2 px-4 border border-gray-300 rounded-md transition-colors duration-200;
}

.btn-danger {
  @apply bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200;
}

.card {
  @apply bg-white overflow-hidden shadow rounded-lg;
}

.card-header {
  @apply px-4 py-5 sm:px-6 border-b border-gray-200;
}

.card-body {
  @apply px-4 py-5 sm:px-6;
}

.input-field {
  @apply mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm;
}

.input-error {
  @apply border-red-500 focus:ring-red-500 focus:border-red-500;
}

.status-badge {
  @apply px-2 py-1 text-xs font-semibold rounded-full;
}

.status-available {
  @apply bg-green-100 text-green-800;
}

.status-low-stock {
  @apply bg-yellow-100 text-yellow-800;
}

.status-out-of-stock {
  @apply bg-red-100 text-red-800;
}
```

### 2. **반응형 디자인**

```css
/* 모바일 최적화 */
@media (max-width: 640px) {
  .sidebar {
    @apply fixed inset-y-0 left-0 z-50 w-64 transform -translate-x-full transition-transform duration-300 ease-in-out;
  }
  
  .sidebar.open {
    @apply translate-x-0;
  }
  
  .main-content {
    @apply pl-0;
  }
}

/* 테이블 반응형 */
.table-responsive {
  @apply overflow-x-auto;
}

.table-responsive table {
  @apply min-w-full divide-y divide-gray-200;
}

/* 로딩 애니메이션 */
.loading-spinner {
  @apply animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600;
}

/* 카드 호버 효과 */
.card:hover {
  @apply shadow-lg transform scale-105 transition-transform duration-200;
}
```

---

## 🚀 사용 방법

### 1. **컴포넌트 import**
```typescript
import Layout from '../components/Layout';
import SupplyList from '../components/SupplyList';
import SupplyForm from '../components/SupplyForm';
import SupplyCard from '../components/SupplyCard';
```

### 2. **페이지 구성**
```typescript
export default function SuppliesPage() {
  const [showForm, setShowForm] = useState(false);
  const [selectedSupply, setSelectedSupply] = useState<Supply | null>(null);

  const handleEdit = (supply: Supply) => {
    setSelectedSupply(supply);
    setShowForm(true);
  };

  const handleDelete = async (supply: Supply) => {
    if (confirm('정말 삭제하시겠습니까?')) {
      // 삭제 API 호출
    }
  };

  const handleFormSubmit = async (supplyData: Partial<Supply>) => {
    // 생성/수정 API 호출
    setShowForm(false);
    setSelectedSupply(null);
  };

  return (
    <Layout>
      <div className="px-4 py-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-900">비품 관리</h1>
          <button
            onClick={() => setShowForm(true)}
            className="btn-primary"
          >
            비품 등록
          </button>
        </div>

        {showForm && (
          <div className="mb-6">
            <SupplyForm
              supply={selectedSupply || undefined}
              onSubmit={handleFormSubmit}
              onCancel={() => {
                setShowForm(false);
                setSelectedSupply(null);
              }}
            />
          </div>
        )}

        <SupplyList
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </div>
    </Layout>
  );
}
```

---

## 🎯 모범 사례

### ✅ **코드 재사용성**
- 컴포넌트 분리 및 props 기반 설계
- 공통 스타일 클래스 활용
- 타입 안전한 TypeScript 사용

### 🚀 **성능 최적화**
- React.memo 사용하여 불필요한 리렌더링 방지
- useCallback으로 함수 최적화
- 이미지 및 정적 자원 최적화

### 🎨 **사용자 경험**
- 로딩 상태 표시
- 에러 메시지 안내
- 반응형 디자인 적용

---

## 🎊 결론

이 컴포넌트 예제들을 통해 완벽한 프론트엔드-백엔드 연동이 가능합니다. 모든 컴포넌트는 실제 프로젝트에서 바로 사용할 수 있도록 구현되었습니다.

**🎯 지금 바로 적용해보세요!**

```bash
# 컴포넌트 파일 복사
cp COMPONENT_EXAMPLES.md frontend/src/components/

# 프로젝트 실행
cd frontend && npm run dev
```

**🌐 http://localhost:3000에서 완벽한 UI를 경험하세요!**
