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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      setError('로그인이 필요합니다.');
      return;
    }

    try {
      const url = selectedSupply 
        ? `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/supplies/${selectedSupply.id}`
        : `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/supplies`;
      
      const method = selectedSupply ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setShowForm(false);
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
        fetchSupplies();
      } else {
        setError(selectedSupply ? '비품 수정에 실패했습니다.' : '비품 생성에 실패했습니다.');
      }
    } catch (err) {
      setError('네트워크 오류가 발생했습니다.');
    }
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

  const handleDelete = async (id: number) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/supplies/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        fetchSupplies();
      } else {
        setError('비품 삭제에 실패했습니다.');
      }
    } catch (err) {
      setError('네트워크 오류가 발생했습니다.');
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
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">비품 관리</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={() => setShowForm(true)}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                비품 추가
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {showForm && (
          <div className="mb-6 bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                {selectedSupply ? '비품 수정' : '비품 추가'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">이름</label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">수량</label>
                    <input
                      type="number"
                      required
                      value={formData.quantity}
                      onChange={(e) => setFormData({...formData, quantity: parseInt(e.target.value)})}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">최소 수량</label>
                    <input
                      type="number"
                      required
                      value={formData.min_quantity}
                      onChange={(e) => setFormData({...formData, min_quantity: parseInt(e.target.value)})}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">단위</label>
                    <input
                      type="text"
                      required
                      value={formData.unit}
                      onChange={(e) => setFormData({...formData, unit: e.target.value})}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">설명</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    rows={3}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">위치</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowForm(false);
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
                    }}
                    className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-md text-sm font-medium"
                  >
                    취소
                  </button>
                  <button
                    type="submit"
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                  >
                    {selectedSupply ? '수정' : '추가'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              비품 목록 ({supplies.length}개)
            </h3>
          </div>
          <div className="grid grid-cols-1 gap-4 p-4 sm:grid-cols-2 lg:grid-cols-3">
            {supplies.map((supply) => (
              <div key={supply.id} className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="text-lg font-medium text-gray-900">{supply.name}</h4>
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    supply.quantity <= supply.min_quantity 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-green-100 text-green-800'
                  }`}>
                    {supply.quantity <= supply.min_quantity ? '저재고' : '정상'}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{supply.description || '설명 없음'}</p>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">수량:</span>
                    <span className="font-medium">{supply.quantity} {supply.unit}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">최소 수량:</span>
                    <span className="font-medium">{supply.min_quantity} {supply.unit}</span>
                  </div>
                  {supply.location && (
                    <div className="flex justify-between">
                      <span className="text-gray-500">위치:</span>
                      <span className="font-medium">{supply.location}</span>
                    </div>
                  )}
                </div>
                <div className="mt-4 flex justify-end space-x-2">
                  <button
                    onClick={() => handleEdit(supply)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
                  >
                    수정
                  </button>
                  <button
                    onClick={() => handleDelete(supply.id)}
                    className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
                  >
                    삭제
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
