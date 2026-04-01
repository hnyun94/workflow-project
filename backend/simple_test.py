#!/usr/bin/env python3
"""
간단한 API 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, Base, engine
from app.models import *
from app.core.security import get_password_hash
from app.models.user import UserRole

def create_test_user():
    """테스트 사용자 생성"""
    db = SessionLocal()
    
    try:
        # 기존 사용자 삭제
        db.query(User).delete()
        db.commit()
        
        # 관리자 생성
        admin = User(
            email="admin@company.com",
            username="관리자",
            hashed_password=get_password_hash("admin123"),
            department="IT팀",
            role=UserRole.ADMIN
        )
        db.add(admin)
        
        # 일반 사용자 생성
        user = User(
            email="user@company.com", 
            username="일반사용자",
            hashed_password=get_password_hash("user123"),
            department="개발팀",
            role=UserRole.USER
        )
        db.add(user)
        
        db.commit()
        print("✅ 테스트 사용자 생성 완료!")
        print("관리자: admin@company.com / admin123")
        print("사용자: user@company.com / user123")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        db.rollback()
    finally:
        db.close()

def create_test_data():
    """테스트 데이터 생성"""
    db = SessionLocal()
    
    try:
        # 카테고리 생성
        cat1 = SupplyCategory(name="전자기기", description="노트북, 모니터 등")
        cat2 = SupplyCategory(name="사무용품", description="펜, 노트 등")
        
        db.add_all([cat1, cat2])
        db.commit()
        
        # 비품 생성
        supply1 = Supply(
            name="노트북",
            description="업무용 노트북",
            category_id=1,
            quantity=10,
            min_quantity=2,
            unit="대",
            location="A창고",
            status="available"
        )
        
        supply2 = Supply(
            name="볼펜",
            description="검정색 볼펜",
            category_id=2,
            quantity=100,
            min_quantity=20,
            unit="개",
            location="B창고",
            status="available"
        )
        
        db.add_all([supply1, supply2])
        db.commit()
        
        print("✅ 테스트 데이터 생성 완료!")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 테스트 데이터 생성
    create_test_user()
    create_test_data()
    
    print("\n🚀 이제 API를 테스트할 수 있습니다!")
    print("📋 Swagger UI: http://localhost:8000/docs")
