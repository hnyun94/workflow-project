#!/usr/bin/env python3
"""
SQLite 데이터베이스 초기화 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models import *

def init_db():
    """데이터베이스 테이블 생성"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def create_sample_data():
    """샘플 데이터 생성"""
    from app.core.database import SessionLocal
    from app.models.user import User, UserRole
    from app.models.supply import SupplyCategory, Supply, SupplyStatus
    from app.core.security import get_password_hash
    
    db = SessionLocal()
    
    try:
        # 관리자 계정 생성
        print("Creating admin user...")
        admin_user = User(
            email="admin@company.com",
            username="관리자",
            hashed_password=get_password_hash("admin123"),
            department="IT팀",
            role=UserRole.ADMIN
        )
        db.add(admin_user)
        
        # 일반 사용자 계정 생성
        print("Creating regular user...")
        regular_user = User(
            email="user@company.com",
            username="일반사용자",
            hashed_password=get_password_hash("user123"),
            department="개발팀",
            role=UserRole.USER
        )
        db.add(regular_user)
        
        # 매니저 계정 생성
        print("Creating manager user...")
        manager_user = User(
            email="manager@company.com",
            username="매니저",
            hashed_password=get_password_hash("manager123"),
            department="운영팀",
            role=UserRole.MANAGER
        )
        db.add(manager_user)
        
        # 카테고리 생성
        print("Creating categories...")
        categories = [
            SupplyCategory(name="전자기기", description="노트북, 모니터 등 전자 장비"),
            SupplyCategory(name="사무용품", description="펜, 노트 등 사무용 소모품"),
            SupplyCategory(name="가구", description="책상, 의자 등 사무용 가구"),
            SupplyCategory(name="네트워크 장비", description="라우터, 스위치 등 네트워크 장비"),
            SupplyCategory(name="청소용품", description="청소기, 휴지 등 청소 관련 용품")
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        
        # 비품 생성
        print("Creating supplies...")
        supplies = [
            Supply(
                name="노트북",
                description="업무용 15인치 노트북",
                category_id=1,
                quantity=10,
                min_quantity=2,
                unit="대",
                location="A창고-1열",
                price=1500000.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="모니터",
                description="24인치 IPS 모니터",
                category_id=1,
                quantity=15,
                min_quantity=3,
                unit="대",
                location="A창고-2열",
                price=350000.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="키보드",
                description="무선 블루투스 키보드",
                category_id=1,
                quantity=20,
                min_quantity=5,
                unit="개",
                location="A창고-3열",
                price=85000.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="A4 노트",
                description="A4 사이즈 100페이지 노트",
                category_id=2,
                quantity=100,
                min_quantity=20,
                unit="권",
                location="B창고-1열",
                price=2000.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="볼펜",
                description="검정색 볼펜",
                category_id=2,
                quantity=200,
                min_quantity=50,
                unit="개",
                location="B창고-1열",
                price=500.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="책상",
                description="4인용 책상",
                category_id=3,
                quantity=5,
                min_quantity=1,
                unit="개",
                location="C창고-1열",
                price=450000.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="의자",
                description="사무용 의자",
                category_id=3,
                quantity=8,
                min_quantity=2,
                unit="개",
                location="C창고-2열",
                price=180000.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="라우터",
                description="유무인 공유기",
                category_id=4,
                quantity=10,
                min_quantity=2,
                unit="대",
                location="A창고-4열",
                price=120000.00,
                status=SupplyStatus.AVAILABLE
            ),
            Supply(
                name="LAN 케이블",
                description="CAT 6 LAN 케이블 5m",
                category_id=4,
                quantity=50,
                min_quantity=10,
                unit="개",
                location="A창고-4열",
                price=8000.00,
                status=SupplyStatus.AVAILABLE
            )
        ]
        
        for supply in supplies:
            db.add(supply)
        
        db.commit()
        print("Sample data created successfully!")
        
        # 생성된 데이터 확인
        print("\n=== 생성된 데이터 ===")
        print(f"사용자 수: {db.query(User).count()}")
        print(f"카테고리 수: {db.query(SupplyCategory).count()}")
        print(f"비품 수: {db.query(Supply).count()}")
        
        print("\n=== 테스트 계정 정보 ===")
        users = db.query(User).all()
        for user in users:
            if user.role == UserRole.ADMIN:
                print(f"관리자 - 이메일: {user.email}, 비밀번호: admin123")
            elif user.role == UserRole.MANAGER:
                print(f"매니저 - 이메일: {user.email}, 비밀번호: manager123")
            else:
                print(f"사용자 - 이메일: {user.email}, 비밀번호: user123")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    create_sample_data()
    print("\n✅ 데이터베이스 초기화 완료!")
    print("이제 API를 사용할 수 있습니다: http://localhost:8000/docs")
