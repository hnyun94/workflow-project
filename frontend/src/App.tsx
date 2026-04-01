import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex items-center justify-center">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              비품 관리 시스템
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Clean Architecture 백엔드 + Lovable 프론트엔드
            </p>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                시스템 접속
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    이메일
                  </label>
                  <input
                    type="email"
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="admin@company.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    비밀번호
                  </label>
                  <input
                    type="password"
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="admin123"
                  />
                </div>
              </div>

              <div className="flex justify-center">
                <button
                  onClick={() => {
                    localStorage.setItem('access_token', 'dummy-token');
                    localStorage.setItem('user', JSON.stringify({
                      id: 1,
                      email: 'admin@company.com',
                      username: '관리자',
                      role: 'admin'
                    }));
                    window.location.href = '/dashboard';
                  }}
                  className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  대시보드로 이동
                </button>
              </div>

              <div className="mt-6 text-sm text-gray-600">
                <p>테스트 계정:</p>
                <ul className="mt-2 space-y-1">
                  <li>관리자: admin@company.com / admin123</li>
                  <li>매니저: manager@company.com / manager123</li>
                  <li>사용자: user@company.com / user123</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
