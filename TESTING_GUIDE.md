# 🧪 프론트엔드-백엔드 통합 테스트 가이드

## 🎯 개요

Lovable 프론트엔드와 Clean Architecture 백엔드의 완벽한 통합을 테스트하는 방법을 상세히 안내합니다.

---

## 🚀 서버 상태 확인

### 1. **서버 실행 상태 확인**
```bash
# 프론트엔드 상태 확인
curl -s http://localhost:3000 | head -5

# 백엔드 상태 확인  
curl -s http://localhost:8000 | head -5

# API 문서 접속 확인
curl -s http://localhost:8000/docs | head -5
```

### 2. **프로세스 확인**
```bash
# 실행 중인 프로세스 확인
ps aux | grep -E "(uvicorn|vite|node)" | grep -v grep

# 포트 사용 확인
lsof -i :3000
lsof -i :8000

# 백엔드 로그 확인
tail -f /tmp/uvicorn.log 2>/dev/null &
```

---

## 🔐 인증 테스트

### 1. **기본 로그인 테스트**
```bash
# 테스트 계정으로 로그인
curl -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@company.com&password=admin123" \
  http://localhost:8000/api/v1/auth/login

# 응답 확인 (성공 시 토큰 반환)
curl -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@company.com&password=admin123" \
  http://localhost:8000/api/v1/auth/login | jq .
```

### 2. **Python 스크립트 테스트**
```python
# test_auth.py
import requests
import json

def test_authentication():
    """인증 시스템 테스트"""
    
    # 테스트 계정
    test_accounts = [
        {"email": "admin@company.com", "password": "admin123", "role": "관리자"},
        {"email": "manager@company.com", "password": "manager123", "role": "매니저"},
        {"email": "user@company.com", "password": "user123", "role": "사용자"}
    ]
    
    for account in test_accounts:
        print(f"\n🧪 {account['role']} 계정 테스트...")
        
        # 로그인 시도
        login_data = {
            'username': account['email'],
            'password': account['password']
        }
        
        response = requests.post('http://localhost:8000/api/v1/auth/login', data=login_data)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print(f"✅ {account['role']} 로그인 성공")
            print(f"🔑 토큰: {token[:20]}...")
            
            # 현재 사용자 정보 확인
            headers = {'Authorization': f'Bearer {token}'}
            user_response = requests.get('http://localhost:8000/api/v1/auth/me', headers=headers)
            
            if user_response.status_code == 200:
                user_data = user_response.json()
                print(f"👤 사용자: {user_data.get('username')} ({user_data.get('role')})")
            else:
                print(f"❌ 사용자 정보 조회 실패: {user_response.status_code}")
        else:
            print(f"❌ {account['role']} 로그인 실패: {response.status_code}")

if __name__ == "__main__":
    test_authentication()
```

### 3. **실행 방법**
```bash
# 백엔드 디렉토리에서 실행
cd backend
python3 test_auth.py
```

---

## 📦 비품 관리 테스트

### 1. **API 직접 테스트**
```bash
# 1. 로그인하여 토큰 받기
TOKEN=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@company.com&password=admin123" \
  http://localhost:8000/api/v1/auth/login | jq -r '.access_token')

echo "🔑 받은 토큰: ${TOKEN:0:50}..."

# 2. 비품 목록 조회
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/supplies | jq .

# 3. 비품 생성
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "테스트 비품",
    "description": "테스트용 비품입니다",
    "quantity": 10,
    "min_quantity": 2,
    "unit": "개",
    "location": "1층 창고",
    "category_id": 1
  }' \
  http://localhost:8000/api/v1/supplies | jq .

# 4. 비품 수정
SUPPLY_ID=1
curl -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "수정된 비품",
    "quantity": 15,
    "description": "수정된 설명"
  }' \
  http://localhost:8000/api/v1/supplies/$SUPPLY_ID | jq .

# 5. 비품 삭제
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/supplies/$SUPPLY_ID
```

### 2. **Python 자동화 테스트**
```python
# test_supplies.py
import requests
import json

def test_supplies_crud():
    """비품 CRUD 기능 테스트"""
    
    # 1. 로그인
    print("🔐 로그인 중...")
    login_response = requests.post(
        'http://localhost:8000/api/v1/auth/login',
        data={'username': 'admin@company.com', 'password': 'admin123'}
    )
    
    if login_response.status_code != 200:
        print(f"❌ 로그인 실패: {login_response.status_code}")
        return
    
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print("✅ 로그인 성공!")
    
    # 2. 비품 목록 조회
    print("\n📦 비품 목록 조회...")
    supplies_response = requests.get('http://localhost:8000/api/v1/supplies', headers=headers)
    
    if supplies_response.status_code == 200:
        supplies = supplies_response.json().get('data', [])
        print(f"📋 현재 비품 수: {len(supplies)}개")
    else:
        print(f"❌ 비품 목록 조회 실패: {supplies_response.status_code}")
        return
    
    # 3. 비품 생성
    print("\n➕ 비품 생성...")
    new_supply = {
        "name": "자동화 테스트 비품",
        "description": "Python 스크립트로 생성된 비품",
        "quantity": 25,
        "min_quantity": 5,
        "unit": "개",
        "location": "자동화 창고",
        "category_id": 1
    }
    
    create_response = requests.post(
        'http://localhost:8000/api/v1/supplies',
        headers=headers,
        json=new_supply
    )
    
    if create_response.status_code == 200:
        created_supply = create_response.json()
        supply_id = created_supply.get('id')
        print(f"✅ 비품 생성 성공: {created_supply.get('name')} (ID: {supply_id})")
    else:
        print(f"❌ 비품 생성 실패: {create_response.status_code}")
        return
    
    # 4. 비품 수정
    print(f"\n✏️ 비품 수정 (ID: {supply_id})...")
    updated_supply = {
        "name": "수정된 자동화 비품",
        "quantity": 30,
        "description": "수정된 설명입니다"
    }
    
    update_response = requests.put(
        f'http://localhost:8000/api/v1/supplies/{supply_id}',
        headers=headers,
        json=updated_supply
    )
    
    if update_response.status_code == 200:
        print("✅ 비품 수정 성공")
    else:
        print(f"❌ 비품 수정 실패: {update_response.status_code}")
    
    # 5. 비품 삭제
    print(f"\n🗑️ 비품 삭제 (ID: {supply_id})...")
    delete_response = requests.delete(
        f'http://localhost:8000/api/v1/supplies/{supply_id}',
        headers=headers
    )
    
    if delete_response.status_code == 200:
        print("✅ 비품 삭제 성공")
    else:
        print(f"❌ 비품 삭제 실패: {delete_response.status_code}")
    
    # 6. 최종 목록 확인
    print("\n📋 최종 비품 목록 확인...")
    final_response = requests.get('http://localhost:8000/api/v1/supplies', headers=headers)
    
    if final_response.status_code == 200:
        final_supplies = final_response.json().get('data', [])
        print(f"📊 최종 비품 수: {len(final_supplies)}개")
    
    print("\n🎉 비품 CRUD 테스트 완료!")

if __name__ == "__main__":
    test_supplies_crud()
```

---

## 🎨 프론트엔드 테스트

### 1. **브라우저 수동 테스트**
```bash
# 1. 브라우저 열기
open http://localhost:3000

# 2. 테스트 시나리오
# - 로그인 페이지 접속
# - 테스트 계정으로 로그인 (admin@company.com / admin123)
# - 대시보드 기능 확인
# - 비품 관리 페이지 이동
# - 비품 생성/수정/삭제 테스트
```

### 2. **자동화 브라우저 테스트**
```python
# test_frontend.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests

def test_frontend_ui():
    """프론트엔드 UI 자동화 테스트"""
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 드라이버 초기화
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("🌐 프론트엔드 접속...")
        driver.get("http://localhost:3000")
        time.sleep(2)
        
        # 페이지 제목 확인
        title = driver.title
        print(f"📄 페이지 제목: {title}")
        
        # 로그인 폼 요소 확인
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.TAG_NAME, "button")
        
        print("✅ 로그인 폼 요소 확인 성공")
        
        # 로그인 정보 입력
        email_input.clear()
        email_input.send_keys("admin@company.com")
        
        password_input.clear()
        password_input.send_keys("admin123")
        
        print("📝 로그인 정보 입력 완료")
        
        # 로그인 버튼 클릭
        login_button.click()
        time.sleep(3)
        
        # 로그인 후 페이지 확인
        current_url = driver.current_url
        print(f"🔄 리디렉션된 URL: {current_url}")
        
        if "dashboard" in current_url.lower():
            print("✅ 로그인 성공 및 대시보드 이동")
            
            # 대시보드 요소 확인
            try:
                user_info = driver.find_element(By.XPATH, "//span[contains(text(), '환영합니다')]")
                print("✅ 사용자 정보 표시 확인")
                
                stats_cards = driver.find_elements(By.CLASS_NAME, "bg-white")
                print(f"📊 통계 카드 수: {len(stats_cards)}")
                
            except Exception as e:
                print(f"⚠️ 대시보드 요소 확인 실패: {e}")
        else:
            print("❌ 로그인 실패 또는 잘못된 리디렉션")
            
    except Exception as e:
        print(f"🚨 테스트 중 오류 발생: {e}")
    finally:
        driver.quit()
        print("🏁 브라우저 드라이버 종료")

if __name__ == "__main__":
    test_frontend_ui()
```

---

## 🔄 통합 테스트

### 1. **종합 테스트 스크립트**
```python
# test_integration.py
import requests
import json
import time

class IntegrationTester:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"
        self.frontend_url = "http://localhost:3000"
        self.token = None
    
    def login(self):
        """로그인하여 토큰 받기"""
        print("🔐 로그인 중...")
        
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={'username': 'admin@company.com', 'password': 'admin123'}
        )
        
        if response.status_code == 200:
            self.token = response.json()['access_token']
            print("✅ 로그인 성공!")
            return True
        else:
            print(f"❌ 로그인 실패: {response.status_code}")
            return False
    
    def test_api_endpoints(self):
        """API 엔드포인트 테스트"""
        if not self.token:
            print("❌ 토큰이 없습니다. 먼저 로그인하세요.")
            return
        
        headers = {'Authorization': f'Bearer {self.token}'}
        
        # 테스트할 엔드포인트 목록
        endpoints = [
            ("GET", "/auth/me", "현재 사용자 정보"),
            ("GET", "/supplies", "비품 목록"),
            ("GET", "/supplies/low-stock/alerts", "저재고 알림"),
        ]
        
        print("\n📡 API 엔드포인트 테스트...")
        
        for method, endpoint, description in endpoints:
            url = f"{self.base_url}{endpoint}"
            
            try:
                response = requests.request(method, url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'data' in data:
                        count = len(data['data'])
                        print(f"✅ {description}: {count}개 항목")
                    else:
                        print(f"✅ {description}: 성공")
                else:
                    print(f"❌ {description}: 실패 ({response.status_code})")
                    
            except Exception as e:
                print(f"🚨 {description}: 예외 발생 - {e}")
    
    def test_frontend_connectivity(self):
        """프론트엔드 연결성 테스트"""
        print(f"\n🌐 프론트엔드 연결 테스트: {self.frontend_url}")
        
        try:
            response = requests.get(self.frontend_url, timeout=5)
            
            if response.status_code == 200:
                print("✅ 프론트엔드 접속 가능")
                
                # 페이지 내용 확인
                content = response.text
                if "비품 관리 시스템" in content:
                    print("✅ 프론트엔드 타이틀 확인")
                if "admin@company.com" in content:
                    print("✅ 테스트 계정 정보 확인")
            else:
                print(f"❌ 프론트엔드 접속 실패: {response.status_code}")
                
        except Exception as e:
            print(f"🚨 프론트엔드 연결 예외: {e}")
    
    def run_full_test(self):
        """전체 통합 테스트 실행"""
        print("🧪 통합 테스트 시작...")
        
        # 1. 프론트엔드 연결 테스트
        self.test_frontend_connectivity()
        
        # 2. 백엔드 로그인 테스트
        if self.login():
            # 3. API 엔드포인트 테스트
            self.test_api_endpoints()
        
        print("\n🎉 통합 테스트 완료!")

if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_full_test()
```

---

## 📊 성능 테스트

### 1. **API 응답 시간 테스트**
```python
# test_performance.py
import requests
import time
import statistics

def test_api_performance():
    """API 성능 테스트"""
    
    # 로그인
    login_response = requests.post(
        'http://localhost:8000/api/v1/auth/login',
        data={'username': 'admin@company.com', 'password': 'admin123'}
    )
    
    if login_response.status_code != 200:
        print("❌ 로그인 실패")
        return
    
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 비품 목록 조회 성능 테스트
    print("📊 비품 목록 조회 성능 테스트...")
    
    response_times = []
    
    for i in range(10):
        start_time = time.time()
        response = requests.get('http://localhost:8000/api/v1/supplies', headers=headers)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # 밀리초로 변환
        response_times.append(response_time)
        
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} 요청 {i+1}: {response_time:.2f}ms")
    
    # 통계
    avg_time = statistics.mean(response_times)
    min_time = min(response_times)
    max_time = max(response_times)
    
    print(f"\n📈 성능 통계:")
    print(f"평균 응답 시간: {avg_time:.2f}ms")
    print(f"최소 응답 시간: {min_time:.2f}ms")
    print(f"최대 응답 시간: {max_time:.2f}ms")

if __name__ == "__main__":
    test_api_performance()
```

---

## 🔧 디버깅 도구

### 1. **실시간 로그 모니터링**
```bash
# 백엔드 로그 실시간 모니터링
tail -f /tmp/uvicorn.log | grep -E "(GET|POST|PUT|DELETE|ERROR)"

# 프론트엔드 빌드 로그 모니터링
cd frontend && npm run dev 2>&1 | grep -E "(ERROR|WARN|built)"
```

### 2. **네트워크 트래픽 분석**
```bash
# 네트워크 연결 상태 확인
netstat -an | grep -E ":3000|:8000"

# 실시간 API 호출 모니터링
sudo tcpdump -i lo -A -s 0 "port 8000" | grep -E "(GET|POST|PUT|DELETE)"
```

---

## 📋 테스트 체크리스트

### ✅ **기본 기능 테스트**
- [ ] 프론트엔드 접속 (http://localhost:3000)
- [ ] 백엔드 API 접속 (http://localhost:8000)
- [ ] API 문서 접속 (http://localhost:8000/docs)
- [ ] 로그인 기능 (3개 계정)
- [ ] JWT 토큰 발급 및 사용
- [ ] 비품 목록 조회
- [ ] 비품 생성 기능
- [ ] 비품 수정 기능
- [ ] 비품 삭제 기능

### ✅ **통합 기능 테스트**
- [ ] 프론트엔드 ↔ 백엔드 API 연동
- [ ] 인증 상태 유지
- [ ] 에러 핸들링
- [ ] 데이터 동기화
- [ ] 실시간 업데이트

### ✅ **성능 테스트**
- [ ] API 응답 시간 측정
- [ ] 동시 접속자 테스트
- [ ] 대용량 데이터 처리
- [ ] 메모리 사용량 모니터링

---

## 🚀 빠른 테스트 명령어

### 1. **일괄 테스트 실행**
```bash
# 전체 테스트 실행
./run_all_tests.sh

# 개별 테스트 실행
./test_auth.sh
./test_supplies.sh
./test_frontend.sh
./test_integration.sh
```

### 2. **테스트 스크립트 생성**
```bash
# run_all_tests.sh
#!/bin/bash

echo "🧪 전체 테스트 시작..."

echo "1️⃣ 인증 테스트..."
python3 test_auth.py

echo "2️⃣ 비품 관리 테스트..."
python3 test_supplies.py

echo "3️⃣ 프론트엔드 테스트..."
python3 test_frontend.py

echo "4️⃣ 통합 테스트..."
python3 test_integration.py

echo "5️⃣ 성능 테스트..."
python3 test_performance.py

echo "🎉 모든 테스트 완료!"
```

---

## 🎯 문제 해결 가이드

### 🔧 **일반적인 문제**
1. **프론트엔드 접속 불가**
   - 포트 충돌 확인: `lsof -i :3000`
   - 방화벽 설정 확인
   - Vite 서버 재시작

2. **백엔드 API 접속 불가**
   - 포트 충돌 확인: `lsof -i :8000`
   - uvicorn 프로세스 확인: `ps aux | grep uvicorn`
   - 데이터베이스 연결 확인

3. **인증 실패**
   - 테스트 데이터 확인: `python3 simple_test.py`
   - 비밀번호 해시 문제 확인
   - JWT 토큰 만료 확인

4. **API 응답 없음**
   - 네트워크 연결 확인
   - CORS 설정 확인
   - 서버 로그 확인

### 🐛 **디버깅 팁**
1. **브라우저 개발자 도구 사용**
   - 네트워크 탭에서 API 호출 확인
   - 콘솔 탭에서 JavaScript 오류 확인
   - 애플리케이션 탭에서 로컬 스토리지 확인

2. **서버 로그 분석**
   - uvicorn 로그: `tail -f /tmp/uvicorn.log`
   - 데이터베이스 로그 확인
   - 시스템 리소스 사용량 확인

3. **API 테스트 도구**
   - Postman 또는 Insomnia 사용
   - curl 명령어로 직접 테스트
   - Python requests 라이브러리 사용

---

## 🎊 성공 기준

### ✅ **모든 테스트 통과 기준**
- 🌐 프론트엔드: 정상 접속 및 UI 렌더링
- 🔐 인증 시스템: 3개 계정 모두 로그인 성공
- 📦 비품 관리: CRUD 기능 모두 정상 작동
- 🔄 API 연동: 프론트엔드-백엔드 완벽 통신
- 📊 데이터 처리: 생성, 조회, 수정, 삭제 모두 성공
- 🎨 UI/UX: 반응형 디자인 및 에러 핸들링

### 📈 **성능 기준**
- ⚡ API 응답 시간: 평균 200ms 이하
- 🔄 페이지 로딩 시간: 3초 이하
- 💾 메모리 사용량: 안정적인 사용량 유지
- 📊 동시 사용자: 10명 이상 처리 가능

---

## 🎉 최종 확인

**🏆 완벽한 통합 테스트 완료!**

이 가이드를 통해 프론트엔드와 백엔드의 완벽한 통합을 체계적으로 테스트할 수 있습니다. 모든 테스트를 통과했다면 성공적인 하이브리드 SaaS 구축이 완료된 것입니다.

**🎯 지금 바로 테스트를 시작해보세요!**
