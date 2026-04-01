#!/bin/bash

echo "🚀 로컬 환경에서 프론트엔드-백엔드 테스트 시작..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. 현재 실행 중인 서비스 확인
echo -e "\n${BLUE}1️⃣ 현재 실행 중인 서비스 확인...${NC}"

# 포트 사용 상태 확인
echo "📡 포트 사용 상태:"
if lsof -i :3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 프론트엔드 (3000) 실행 중${NC}"
    FRONTEND_RUNNING=true
else
    echo -e "${RED}❌ 프론트엔드 (3000) 실행되지 않음${NC}"
    FRONTEND_RUNNING=false
fi

if lsof -i :8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 백엔드 (8000) 실행 중${NC}"
    BACKEND_RUNNING=true
else
    echo -e "${RED}❌ 백엔드 (8000) 실행되지 않음${NC}"
    BACKEND_RUNNING=false
fi

# 2. 서비스 시작 (필요한 경우)
if [ "$FRONTEND_RUNNING" = false ]; then
    echo -e "\n${YELLOW}🎨 프론트엔드 서비스 시작...${NC}"
    cd frontend
    npm run dev > /tmp/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "프론트엔드 PID: $FRONTEND_PID"
    cd ..
    sleep 5
fi

if [ "$BACKEND_RUNNING" = false ]; then
    echo -e "\n${YELLOW}⚙️ 백엔드 서비스 시작...${NC}"
    cd backend
    python3 -m uvicorn main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
    BACKEND_PID=$!
    echo "백엔드 PID: $BACKEND_PID"
    cd ..
    sleep 5
fi

# 3. 서비스 상태 재확인
echo -e "\n${BLUE}2️⃣ 서비스 상태 재확인...${NC}"

# 프론트엔드 상태 확인
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 프론트엔드 접속 가능${NC}"
    FRONTEND_OK=true
else
    echo -e "${RED}❌ 프론트엔드 접속 불가${NC}"
    FRONTEND_OK=false
fi

# 백엔드 상태 확인
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 백엔드 접속 가능${NC}"
    BACKEND_OK=true
else
    echo -e "${RED}❌ 백엔드 접속 불가${NC}"
    BACKEND_OK=false
fi

# 4. API 문서 접속 확인
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API 문서 접속 가능${NC}"
    DOCS_OK=true
else
    echo -e "${RED}❌ API 문서 접속 불가${NC}"
    DOCS_OK=false
fi

# 5. 통합 테스트 실행
if [ "$BACKEND_OK" = true ] && [ "$FRONTEND_OK" = true ]; then
    echo -e "\n${BLUE}3️⃣ 통합 테스트 실행...${NC}"
    
    # 테스트용 Python 스크립트 생성
    cat > test_local_integration.py << 'EOF'
import requests
import json
import time

def run_integration_tests():
    """로컬 통합 테스트"""
    base_url = "http://localhost:8000/api/v1"
    frontend_url = "http://localhost:3000"
    
    print("🔐 인증 테스트...")
    
    # 로그인 테스트
    test_accounts = [
        {"email": "admin@company.com", "password": "admin123", "role": "관리자"},
        {"email": "manager@company.com", "password": "manager123", "role": "매니저"},
        {"email": "user@company.com", "password": "user123", "role": "사용자"}
    ]
    
    for account in test_accounts:
        print(f"🧪 {account['role']} 계정 테스트...")
        
        response = requests.post(
            f"{base_url}/auth/login",
            data={'username': account['email'], 'password': account['password']},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print(f"✅ {account['role']} 로그인 성공")
            
            # 비품 목록 조회 테스트
            headers = {'Authorization': f'Bearer {token}'}
            supplies_response = requests.get(f"{base_url}/supplies", headers=headers, timeout=5)
            
            if supplies_response.status_code == 200:
                supplies = supplies_response.json().get('data', [])
                print(f"📦 비품 목록: {len(supplies)}개")
                
                # 비품 생성 테스트
                new_supply = {
                    "name": f"로컬 테스트 비품 ({account['role']})",
                    "description": f"{account['role']}용 테스트 비품",
                    "quantity": 10,
                    "min_quantity": 2,
                    "unit": "개",
                    "category_id": 1
                }
                
                create_response = requests.post(
                    f"{base_url}/supplies",
                    headers=headers,
                    json=new_supply,
                    timeout=5
                )
                
                if create_response.status_code == 200:
                    created = create_response.json()
                    print(f"✅ 비품 생성 성공: {created.get('name')}")
                else:
                    print(f"❌ 비품 생성 실패: {create_response.status_code}")
            else:
                print(f"❌ 비품 목록 조회 실패: {supplies_response.status_code}")
        else:
            print(f"❌ {account['role']} 로그인 실패: {response.status_code}")
    
    print("\n🎨 프론트엔드 연결 테스트...")
    
    # 프론트엔드 접속 테스트
    try:
        frontend_response = requests.get(frontend_url, timeout=5)
        if frontend_response.status_code == 200:
            content = frontend_response.text
            if "비품 관리 시스템" in content:
                print("✅ 프론트엔드 접속 가능")
                print("✅ 프론트엔드 타이틀 확인")
            else:
                print("⚠️ 프론트엔드 접속 가능하나 타이틀 이상")
        else:
            print(f"❌ 프론트엔드 접속 실패: {frontend_response.status_code}")
    except Exception as e:
        print(f"❌ 프론트엔드 연결 예외: {e}")
    
    print("\n🎉 통합 테스트 완료!")

if __name__ == "__main__":
    run_integration_tests()
EOF

    # 통합 테스트 실행
    python3 test_local_integration.py
    
else
    echo -e "\n${RED}❌ 서비스가 정상적으로 실행되지 않아 통합 테스트를 실행할 수 없습니다.${NC}"
    echo -e "${YELLOW}서비스 상태:${NC}"
    echo -e "  프론트엔드: $([ "$FRONTEND_OK" = true ] && echo "✅ 정상" || echo "❌ 비정상")"
    echo -e "  백엔드: $([ "$BACKEND_OK" = true ] && echo "✅ 정상" || echo "❌ 비정상")"
    echo -e "  API 문서: $([ "$DOCS_OK" = true ] && echo "✅ 정상" || echo "❌ 비정상")"
fi

# 6. 로그 보기 옵션
echo -e "\n${BLUE}4️⃣ 로그 보기${NC}"
echo "프론트엔드 로그: tail -f /tmp/frontend.log"
echo "백엔드 로그: tail -f /tmp/backend.log"
echo ""
echo -e "${GREEN}🌐 접속 정보:${NC}"
echo "프론트엔드: http://localhost:3000"
echo "백엔드 API: http://localhost:8000"
echo "API 문서: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}🛑 서비스 중지: Ctrl+C${NC}"

# 7. 정리 함수
cleanup() {
    echo -e "\n${YELLOW}🛑 서비스 정리 중...${NC}"
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "프론트엔드 서비스 중지"
    fi
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "백엔드 서비스 중지"
    fi
    
    echo -e "${GREEN}✅ 모든 서비스 정리 완료${NC}"
    exit 0
}

# 시그널 핸들러
trap cleanup SIGINT SIGTERM

# 대기 (사용자가 Ctrl+C를 누를 때까지)
echo -e "\n${BLUE}⏸ 테스트 실행 중... (Ctrl+C로 종료)${NC}"
while true; do
    sleep 1
done
