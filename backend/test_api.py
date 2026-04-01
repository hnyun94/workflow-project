#!/usr/bin/env python3
"""
API 테스트 스크립트
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """헬스 체크"""
    response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
    print(f"Health Check: {response.status_code} - {response.json()}")

def test_register():
    """회원가입 테스트"""
    user_data = {
        "email": "test@company.com",
        "username": "테스트사용자",
        "password": "test123",
        "department": "개발팀",
        "role": "user"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Register: {response.status_code}")
    if response.status_code == 200:
        print(f"User created: {response.json()}")
    else:
        print(f"Error: {response.text}")

def test_login():
    """로그인 테스트"""
    login_data = {
        "username": "test@company.com",
        "password": "test123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        print(f"Token received: {token_data['access_token'][:50]}...")
        return token_data['access_token']
    else:
        print(f"Error: {response.text}")
        return None

def test_categories(token):
    """카테고리 조회 테스트"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/categories", headers=headers)
    print(f"Categories: {response.status_code}")
    if response.status_code == 200:
        categories = response.json()
        print(f"Found {len(categories)} categories")
        for cat in categories:
            print(f"  - {cat['name']}: {cat['description']}")

def test_supplies(token):
    """비품 목록 조회 테스트"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/supplies", headers=headers)
    print(f"Supplies: {response.status_code}")
    if response.status_code == 200:
        supplies = response.json()
        print(f"Found {len(supplies)} supplies")
        for supply in supplies[:3]:  # 처음 3개만 표시
            print(f"  - {supply['name']}: {supply['quantity']}개 ({supply['status']})")

def test_create_supply(token):
    """비품 생성 테스트"""
    headers = {"Authorization": f"Bearer {token}"}
    supply_data = {
        "name": "테스트 비품",
        "description": "API 테스트용 비품",
        "category_id": 1,
        "quantity": 5,
        "min_quantity": 1,
        "unit": "개",
        "location": "테스트 창고"
    }
    
    response = requests.post(f"{BASE_URL}/supplies", json=supply_data, headers=headers)
    print(f"Create Supply: {response.status_code}")
    if response.status_code == 200:
        supply = response.json()
        print(f"Created: {supply['name']} (ID: {supply['id']})")
        return supply['id']
    else:
        print(f"Error: {response.text}")
        return None

def main():
    print("🚀 API 테스트 시작...\n")
    
    # 헬스 체크
    test_health()
    print()
    
    # 회원가입
    test_register()
    print()
    
    # 로그인
    token = test_login()
    print()
    
    if token:
        # 카테고리 조회
        test_categories(token)
        print()
        
        # 비품 목록 조회
        test_supplies(token)
        print()
        
        # 비품 생성 (권한 테스트)
        test_create_supply(token)
        print()
    
    print("✅ API 테스트 완료!")
    print("\n📋 API 문서: http://localhost:8000/docs")
    print("🔑 테스트 계정:")
    print("  - 관리자: admin@company.com / admin123")
    print("  - 매니저: manager@company.com / manager123") 
    print("  - 사용자: user@company.com / user123")

if __name__ == "__main__":
    main()
