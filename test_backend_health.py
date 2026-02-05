"""
Quick backend health check
"""
import requests
import time

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🏥 Backend Health Check")
print("=" * 60)

# Test 1: Basic health
print("\n1. Testing basic health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print(f"✅ Backend is running: {response.json()}")
    else:
        print(f"❌ Backend returned status {response.status_code}")
except Exception as e:
    print(f"❌ Cannot connect to backend: {e}")
    print("\n⚠️  Make sure backend is running:")
    print("   cd backend")
    print("   python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000")
    exit(1)

# Test 2: OpenAI health
print("\n2. Testing OpenAI API connection...")
try:
    response = requests.get(f"{BASE_URL}/api/health/openai", timeout=20)
    data = response.json()
    
    print(f"Status: {data['status']}")
    print(f"Message: {data['message']}")
    print(f"OpenAI Configured: {data['openai_configured']}")
    print(f"OpenAI Working: {data['openai_working']}")
    
    if data['openai_working']:
        print("\n✅ OpenAI API is working! Agent should work fine.")
    else:
        print("\n❌ OpenAI API is not working!")
        print("Possible issues:")
        print("  - Invalid API key")
        print("  - Network/firewall blocking OpenAI")
        print("  - OpenAI API is down")
        print("\nCheck your .env file and make sure OPENAI_API_KEY is correct")
        
except Exception as e:
    print(f"❌ Error checking OpenAI: {e}")

print("\n" + "=" * 60)
