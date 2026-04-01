#!/usr/bin/env python3
"""
데모용 API 테스트
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def demo():
    print("🚀 비품 관리 시스템 API 데모\n")
    
    # 1. 로그인
    print("1️⃣ 관리자 로그인...")
    login_data = {
        "username": "admin@company.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ 로그인 성공!")
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print("❌ 로그인 실패")
        return
    
    # 2. 카테고리 조회
    print("\n2️⃣ 카테고리 조회...")
    response = requests.get(f"{BASE_URL}/categories/", headers=headers)
    if response.status_code == 200:
        categories = response.json()
        print(f"✅ {len(categories)}개 카테고리 발견:")
        for cat in categories:
            print(f"   - {cat['name']}: {cat['description']}")
    else:
        print(f"❌ 카테고리 조회 실패: {response.text}")
    
    # 3. 비품 생성
    print("\n3️⃣ 새 비품 등록...")
    supply_data = {
        "name": "데모 노트북",
        "description": "데모용 노트북",
        "category_id": 1,
        "quantity": 5,
        "min_quantity": 1,
        "unit": "대",
        "location": "데모 창고"
    }
    
    response = requests.post(f"{BASE_URL}/supplies/", json=supply_data, headers=headers)
    if response.status_code == 200:
        supply = response.json()
        print(f"✅ 비품 등록 성공: {supply['name']} (ID: {supply['id']})")
        supply_id = supply['id']
    else:
        print(f"❌ 비품 등록 실패: {response.text}")
        return
    
    # 4. 비품 목록 조회
    print("\n4️⃣ 비품 목록 조회...")
    response = requests.get(f"{BASE_URL}/supplies/", headers=headers)
    if response.status_code == 200:
        supplies = response.json()
        print(f"✅ {len(supplies)}개 비품 발견:")
        for supply in supplies:
            print(f"   - {supply['name']}: {supply['quantity']}개 ({supply['status']})")
    else:
        print(f"❌ 비품 목록 조회 실패: {response.text}")
    
    # 5. 입고 처리
    print("\n5️⃣ 입고 처리...")
    transaction_data = {
        "supply_id": supply_id,
        "transaction_type": "in",
        "quantity": 3,
        "notes": "데모 입고"
    }
    
    response = requests.post(f"{BASE_URL}/transactions/", json=transaction_data, headers=headers)
    if response.status_code == 200:
        print("✅ 입고 처리 성공!")
    else:
        print(f"❌ 입고 처리 실패: {response.text}")
    
    # 6. 비품 상세 조회 (재고 확인)
    print("\n6️⃣ 비품 상세 조회...")
    response = requests.get(f"{BASE_URL}/supplies/{supply_id}", headers=headers)
    if response.status_code == 200:
        supply = response.json()
        print(f"✅ 현재 재고: {supply['quantity']}개")
    else:
        print(f"❌ 상세 조회 실패: {response.text}")
    
    # 7. 예약 생성
    print("\n7️⃣ 비품 예약...")
    from datetime import datetime, timedelta
    start_time = datetime.now() + timedelta(hours=1)
    end_time = datetime.now() + timedelta(days=1)
    
    reservation_data = {
        "supply_id": supply_id,
        "quantity": 1,
        "start_date": start_time.isoformat(),
        "end_date": end_time.isoformat(),
        "purpose": "데모용 예약"
    }
    
    response = requests.post(f"{BASE_URL}/reservations/", json=reservation_data, headers=headers)
    if response.status_code == 200:
        reservation = response.json()
        print(f"✅ 예약 성공: ID {reservation['id']}")
    else:
        print(f"❌ 예약 실패: {response.text}")
    
    print("\n🎉 데모 완료!")
    print("\n📋 주요 기능:")
    print("   ✅ JWT 인증")
    print("   ✅ 비품 CRUD")
    print("   ✅ 재고 관리")
    print("   ✅ 예약 시스템")
    print("   ✅ 거래 기록")
    
    print(f"\n🌐 API 문서: http://localhost:8000/docs")
    print(f"🔑 테스트 계정: admin@company.com / admin123")

if __name__ == "__main__":
    demo()
