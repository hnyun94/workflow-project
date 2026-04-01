# 🚀 로컬 테스트 빠른 시작 가이드

## 🎯 개요

로컬 환경에서 프론트엔드-백엔드 통합 서비스를 테스트하는 가장 빠른 방법을 안내합니다.

---

## ⚡ 1분 만에 시작하기

### 1️⃣ **자동화 스크립트 실행**
```bash
# 프로젝트 루트에서 실행
./run_local_tests.sh
```

이 명령어 하나로:
- ✅ 서비스 상태 확인
- ✅ 필요한 서비스 자동 시작
- ✅ 통합 테스트 자동 실행
- ✅ 실시간 로그 모니터링

---

## 📋 수동 테스트 방법

### 1️⃣ **서비스 상태 확인**
```bash
# 포트 사용 상태 확인
lsof -i :3000 :8000

# 서비스 실행 상태 확인
ps aux | grep -E "(uvicorn|vite|node)"
```

### 2️⃣ **서비스 시작**
```bash
# 프론트엔드 시작
cd frontend
npm run dev &

# 백엔드 시작
cd backend
python3 -m uvicorn main:app --reload --port 8000 &
```

### 3️⃣ **브라우저 테스트**
```bash
# 프론트엔드 접속
open http://localhost:3000

# API 문서 접속
open http://localhost:8000/docs
```

---

## 🔐 테스트 계정

| 역할 | 이메일 | 비밀번호 | 권한 |
|------|--------|----------|------|
| 👑 관리자 | admin@company.com | admin123 | 전체 권한 |
| 👨‍💼 매니저 | manager@company.com | manager123 | 비품 관리 |
| 👤 사용자 | user@company.com | user123 | 조회만 가능 |

---

## 🧪 테스트 시나리오

### ✅ **기본 기능 테스트**
1. **로그인 테스트**
   - 3개 계정 모두 로그인 시도
   - JWT 토큰 발급 확인
   - 사용자 정보 표시 확인

2. **대시보드 테스트**
   - 통계 카드 표시 확인
   - 비품 목록 표시 확인
   - 저재고 알림 확인

3. **비품 관리 테스트**
   - 비품 생성 기능
   - 비품 수정 기능
   - 비품 삭제 기능
   - 데이터 실시간 동기화

---

## 🔧 문제 해결

### 🚨 **일반적인 문제**
1. **포트 충돌**
   ```bash
   # 포트 사용 확인
   lsof -i :3000 :8000
   
   # 프로세스 강제 종료
   kill -9 $(lsof -ti:3000)
   kill -9 $(lsof -ti:8000)
   ```

2. **서비스 시작 실패**
   ```bash
   # 의존성 설치 확인
   cd frontend && npm install
   cd backend && python3 -m pip install -r requirements.txt
   
   # 권한 문제 해결
   chmod +x run_local_tests.sh
   ```

3. **인증 실패**
   ```bash
   # 테스트 데이터 재생성
   cd backend && python3 simple_test.py
   
   # 데이터베이스 초기화
   rm -f supplies.db
   python3 simple_test.py
   ```

---

## 📊 성공 확인

### ✅ **성공 기준**
- 🌐 **프론트엔드**: http://localhost:3000 접속 가능
- ⚙️ **백엔드**: http://localhost:8000 접속 가능
- 📚 **API 문서**: http://localhost:8000/docs 접속 가능
- 🔐 **인증**: 3개 계정 모두 로그인 성공
- 📦 **비품 관리**: CRUD 기능 모두 정상 작동
- 🔄 **데이터 동기화**: 프론트엔드-백엔드 실시간 연동

### 📈 **성능 기준**
- ⚡ **API 응답**: 평균 200ms 이하
- 🔄 **페이지 로딩**: 3초 이하
- 💾 **메모리 사용**: 안정적인 사용량 유지

---

## 🎯 빠른 테스트 명령어

### 🚀 **한 번에 실행**
```bash
# 전체 테스트 (가장 빠름)
./run_local_tests.sh

# 개별 테스트
curl -s http://localhost:3000  # 프론트엔드
curl -s http://localhost:8000  # 백엔드
curl -s http://localhost:8000/docs  # API 문서
```

### 🔍 **상세 확인**
```bash
# 서비스 상태 상세 확인
netstat -an | grep -E ":3000|:8000"

# 로그 실시간 확인
tail -f /tmp/frontend.log &  # 프론트엔드
tail -f /tmp/backend.log &   # 백엔드
```

---

## 🎉 완료 확인

### ✅ **모든 테스트 통과 시**
- 🏆 **완벽한 하이브리드 SaaS** 구축 성공
- 🎨 **현대적 UI/UX** 구현 완료
- 🔗 **완벽한 API 연동** 성공
- 📊 **실시간 데이터 처리** 성공
- 🚀 **프로덕션 준비** 완료

---

## 📞 도움말

### 🆘 **문제 발생 시**
1. **서버 재시작**
   ```bash
   # 모든 서비스 중지
   kill $(lsof -ti:3000) 2>/dev/null
   kill $(lsof -ti:8000) 2>/dev/null
   
   # 스크립트로 재시작
   ./run_local_tests.sh
   ```

2. **데이터 초기화**
   ```bash
   # 데이터베이스 삭제 후 재생성
   cd backend
   rm -f supplies.db
   python3 simple_test.py
   ```

3. **로그 분석**
   ```bash
   # 에러 로그 확인
   grep -i error /tmp/backend.log
   grep -i error /tmp/frontend.log
   ```

---

## 🎊 결론

**🏆 로컬 테스트는 이제 1분이면 충분합니다!**

✅ **자동화 스크립트**: `./run_local_tests.sh`  
✅ **수동 테스트**: 브라우저 및 API 직접 테스트  
✅ **문제 해결**: 빠른 진단 및 해결 가이드  
✅ **성공 확인**: 명확한 기준 및 체크리스트  

---

**🚀 지금 바로 시작해보세요!**

```bash
cd /Users/hnyun/workspace/study/project3
./run_local_tests.sh
```

**🌐 테스트 접속 정보**
- 프론트엔드: http://localhost:3000
- 백엔드: http://localhost:8000
- API 문서: http://localhost:8000/docs

**🎯 완벽한 하이브리드 SaaS 테스트를 지금 바로 경험하세요!**
