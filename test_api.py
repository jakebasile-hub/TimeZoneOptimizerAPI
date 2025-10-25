#!/usr/bin/env python3
"""
Simple test script to verify the TimeZone Optimizer API is working
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}, uptime: {data['uptime']:.2f}s")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def create_api_key():
    """Create a test API key"""
    print("🔑 Creating test API key...")
    try:
        response = requests.post(f"{API_BASE}/create-key", params={"user_id": "test_user"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API key created: {data['api_key']}")
            return data['api_key']
        else:
            print(f"❌ Failed to create API key: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ API key creation error: {e}")
        return None

def test_optimize(api_key):
    """Test optimize endpoint"""
    print("🌍 Testing optimize endpoint...")
    
    test_data = {
        "participants": [
            {"name": "Alice", "location": "New York, USA"},
            {"name": "Bob", "location": "London, UK"},
            {"name": "Cara", "location": "Tokyo, Japan"}
        ],
        "duration_minutes": 60,
        "num_alternatives": 2
    }
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_BASE}/optimize", json=test_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Optimize endpoint working!")
            print(f"   Best time: {data['best_meeting_time_utc']}")
            print(f"   Local times: {len(data['local_times'])} participants")
            print(f"   Alternatives: {len(data['alternatives'])} options")
            return True
        else:
            print(f"❌ Optimize endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Optimize endpoint error: {e}")
        return False

def main():
    print("🧪 TimeZone Optimizer API Test Suite")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("❌ API is not running. Please start it with: python run.py")
        return
    
    # Create API key
    api_key = create_api_key()
    if not api_key:
        print("❌ Cannot proceed without API key")
        return
    
    # Test optimize endpoint
    if test_optimize(api_key):
        print("\n🎉 All tests passed! API is working correctly.")
        print("📚 Visit http://localhost:8000/docs for interactive API documentation")
        print("🌐 Open frontend/index.html in your browser for the web interface")
    else:
        print("\n❌ Some tests failed. Check the API logs for details.")

if __name__ == "__main__":
    main()
