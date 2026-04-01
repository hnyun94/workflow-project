import React, { useState, useEffect } from 'react';

interface Supply {
  id: number;
  name: string;
  description?: string;
  quantity: number;
  min_quantity: number;
  unit: string;
  location?: string;
  status: string;
  category?: {
    id: number;
    name: string;
  };
  created_at: string;
}

export default function SuppliesPage() {
  const [supplies, setSupplies] = useState<Supply[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [selectedSupply, setSelectedSupply] = useState<Supply | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    quantity: 0,
    min_quantity: 1,
    unit: '개',
    location: '',
    category_id: 1,
  });

  useEffect(() => {
    fetchSupplies();
  }, []);

  const fetchSupplies = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/supplies`, {
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

  const handleCreate = () => {
    setSelectedSupply(null);
    setFormData({
      name: '',
      description: '',
      quantity: 0,
      min_quantity: 1,
      unit: '개',
      location: '',
      category_id: 1,
    });
    setShowForm(true);
  };

  const handleEdit = (supply: Supply) => {
    setSelectedSupply(supply);
    setFormData({
      name: supply.name,
      description: supply.description || '',
      quantity: supply.quantity,
      min_quantity: supply.min_quantity,
      unit: supply.unit,
      location: supply.location || '',
      category_id: supply.category?.id || 1,
    });
    setShowForm(true);
  };

  const handleDelete = async (supply: Supply) => {
    if (confirm('정말 삭제하시겠습니까?')) {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/supplies/${supply.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            fetchSupplies(); // 목록 새로고침
          } else {
            setError('삭제에 실패했습니다.');
          }
        }
      } catch (err) {
        setError('네트워크 오류가 발생했습니다.');
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        const url = selectedSupply 
          ? `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/supplies/${selectedSupply.id}`
          : `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/supplies`;
        
        const response = await fetch(url, {
          method: selectedSupply ? 'PUT' : 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          setShowForm(false);
          setSelectedSupply(null);
          fetchSupplies(); // 목록 새로고침
        } else {
          setError(selectedSupply ? '수정에 실패했습니다.' : '등록에 실패했습니다.');
        }
      }
    } catch (err) {
      setError('네트워크 오류가 발생했습니다.');
    }
  };

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
              <h1 className="text-xl font-semibold">비품 관리</h1>
            </div>
            <button
              onClick={handleCreate}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              비품 등록
            </button>
          </div>
        </div>
      </header>

      {/* 메인 콘텐츠 */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {showForm && (
          <div className="mb-6 bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                {selectedSupply ? '비품 수정' : '비품 등록'}
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
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      placeholder="예: A4 용지"
                      required
                    />
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
                      onChange={(e) => setFormData({...formData, quantity: Number(e.target.value)})}
                      min="0"
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      required
                    />
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
                      onChange={(e) => setFormData({...formData, min_quantity: Number(e.target.value)})}
                      min="0"
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      required
                    />
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
                      onChange={(e) => setFormData({...formData, unit: e.target.value})}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      placeholder="예: 개, 박스, 병"
                      required
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
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
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
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    rows={3}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="비품에 대한 상세 설명"
                  />
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => setShowForm(false)}
                    className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    취소
                  </button>
                  <button
                    type="submit"
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    {selectedSupply ? '수정' : '등록'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* 비품 목록 */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              비품 목록 ({supplies.length}개)
            </h3>
            
            {supplies.length === 0 ? (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414-2.414a1 1 0 00-.707 0l-2.414 2.414a1 1 0 00.293.707L16.586 13H18a2 2 0 002 2z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">등록된 비품이 없습니다</h3>
                <p className="mt-1 text-sm text-gray-500">첫 번째 비품을 등록해보세요.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {supplies.map((supply) => (
                  <div key={supply.id} className="bg-white overflow-hidden shadow rounded-lg">
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

                      <div className="mt-6 flex justify-between">
                        <div className="text-sm text-gray-500">
                          생성일: {new Date(supply.created_at).toLocaleDateString()}
                        </div>
                        
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEdit(supply)}
                            className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                          >
                            수정
                          </button>
                          
                          <button
                            onClick={() => handleDelete(supply)}
                            className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                          >
                            삭제
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
