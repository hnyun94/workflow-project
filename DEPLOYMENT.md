# 배포 가이드

## 로컬 개발 환경 설정

### 1. 데이터베이스 설정
```bash
# PostgreSQL 설치 (macOS)
brew install postgresql
brew services start postgresql

# 데이터베이스 생성
createdb supplies_db

# 사용자 생성 (선택사항)
createuser -s postgres
```

### 2. 백엔드 설정
```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에서 데이터베이스 연결 정보 수정

# 데이터베이스 마이그레이션
alembic upgrade head

# 초기 데이터 삽입
psql -d supplies_db -f ../init.sql

# 개발 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Docker를 사용한 전체 시스템 실행
```bash
# 프로젝트 루트에서
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

## 프로덕션 배포

### 1. 클라우드 서버 설정 (AWS EC2 예시)

#### 서버 기본 설정
```bash
# Ubuntu 22.04 LTS
sudo apt update && sudo apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 방화벽 설정
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

#### 프로젝트 배포
```bash
# Git 클론
git clone <your-repository-url>
cd project3

# 환경 변수 설정
cp .env.example .env
# .env 파일을 프로덕션 환경에 맞게 수정

# SSL 인증서 설정 (Let's Encrypt)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Docker Compose 실행
docker-compose -f docker-compose.prod.yml up -d --build
```

### 2. 프로덕션 Docker Compose 설정

**docker-compose.prod.yml**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: supplies_db_prod
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - supplies_network
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: supplies_backend_prod
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - postgres
    networks:
      - supplies_network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: supplies_frontend_prod
    environment:
      - REACT_APP_API_URL=https://yourdomain.com/api/v1
    depends_on:
      - backend
    networks:
      - supplies_network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: supplies_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - supplies_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  supplies_network:
    driver: bridge
```

### 3. Nginx 설정

**nginx/nginx.conf**:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS configuration
    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://backend/health;
        }
    }
}
```

### 4. 프로덕션 Dockerfile

**backend/Dockerfile.prod**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 비프로덕션 모듈 제거
RUN pip uninstall -y pytest pytest-asyncio httpx

# Gunicorn 설치
RUN pip install gunicorn

# 포트 노출
EXPOSE 8000

# Gunicorn으로 실행
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

**frontend/Dockerfile.prod**:
```dockerfile
# Build stage
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 모니터링 및 로깅

### 1. 로그 수집
```bash
# Docker 로그 확인
docker-compose logs -f backend
docker-compose logs -f frontend

# 로그 파일 저장
docker-compose logs --no-color > logs.txt
```

### 2. 헬스 체크 스크립트
**scripts/health-check.sh**:
```bash
#!/bin/bash

# API 헬스 체크
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ $response -eq 200 ]; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend is unhealthy (HTTP $response)"
    exit 1
fi

# 프론트엔드 헬스 체크
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)

if [ $response -eq 200 ]; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is unhealthy (HTTP $response)"
    exit 1
fi

echo "✅ All services are healthy"
```

### 3. 자동 백업 스크립트
**scripts/backup.sh**:
```bash
#!/bin/bash

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="supplies_db"

# 백업 디렉토리 생성
mkdir -p $BACKUP_DIR

# 데이터베이스 백업
docker exec supplies_db_prod pg_dump -U postgres $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# 7일 이상 된 백업 삭제
find $BACKUP_DIR -name "db_backup_*.sql" -mtime +7 -delete

echo "Database backup completed: $BACKUP_DIR/db_backup_$DATE.sql"
```

## 보안 고려사항

### 1. 환경 변수 관리
- `.env` 파일은 절대 Git에 커밋하지 않음
- 프로덕션 환경에서는 보안 도구(HashiCorp Vault, AWS Secrets Manager) 사용

### 2. 데이터베이스 보안
- 강력한 비밀번호 사용
- 데이터베이스 접속 IP 제한
- 정기적인 백업 및 암호화

### 3. API 보안
- JWT 토큰 만료 시간 설정
- Rate limiting 구현
- HTTPS 강제 사용

### 4. 네트워크 보안
- 방화벽 설정
- 불필요한 포트 닫기
- VPN 또는 VPC 사용

## 문제 해결

### 1. 공통 문제
```bash
# 컨테이너 재시작
docker-compose restart

# 이미지 재빌드
docker-compose up --build --force-recreate

# 로그 확인
docker-compose logs <service_name>

# 컨테이너 접속
docker exec -it <container_name> bash
```

### 2. 데이터베이스 연결 문제
- 데이터베이스 서버 상태 확인
- 네트워크 연결 확인
- 인증 정보 확인

### 3. CORS 문제
- 프론트엔드 도메인이 CORS 허용 목록에 있는지 확인
- API 요청에 올바른 헤더가 포함되어 있는지 확인

이 배포 가이드를 따라 하이브리드 SaaS 비품 관리 시스템을 성공적으로 배포할 수 있습니다.
