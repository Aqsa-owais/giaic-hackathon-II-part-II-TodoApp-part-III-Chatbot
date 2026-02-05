"""
Direct Agent API Test - Tests backend agent endpoint
"""
import requests
import json
import uuid
import time

BASE_URL = "http://localhost:8000"

def test_agent():
    print("=" * 70)
    print("🤖 DIRECT AGENT API TEST")
    print("=" * 70)
    
    # Step 1: Register
    print("\n1. Registering user...")
    email = f'test{uuid.uuid4().hex[:6]}@example.com'
    password = 'TestPass123!'
    
    try:
        resp = requests.post(f'{BASE_URL}/api/register', 
                            json={'email': email, 'password': password},
                            timeout=10)
        if resp.status_code != 201:
            print(f"❌ Register failed: {resp.text}")
            return
        user_id = resp.json()['id']
        print(f"✅ User registered: {user_id}")
    except Exception as e:
        print(f"❌ Register error: {e}")
        print("\n⚠️  Backend not running! Start it with:")
        print("   cd backend")
        print("   python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Step 2: Login
    print("\n2. Logging in...")
    try:
        resp = requests.post(f'{BASE_URL}/api/login',
                            json={'email': email, 'password': password},
                            timeout=10)
        if resp.status_code != 200:
            print(f"❌ Login failed: {resp.text}")
            return
        token = resp.json()['access_token']
        print(f"✅ Logged in: {token[:20]}...")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Step 3: Test Agent - Create Task
    print("\n3. Testing Agent - Create Task...")
    print("   Message: 'Create a task to buy groceries'")
    print("   ⏳ Waiting for OpenAI response (may take 10-30 seconds)...")
    
    start_time = time.time()
    
    try:
        resp = requests.post(
            f'{BASE_URL}/api/v1/users/{user_id}/chat',
            headers=headers,
            json={'message': 'Create a task to buy groceries'},
            timeout=60  # 60 second timeout
        )
        
        elapsed = time.time() - start_time
        print(f"   ⏱️  Response time: {elapsed:.2f}s")
        
        if resp.status_code != 200:
            print(f"❌ Agent failed: {resp.status_code}")
            print(f"   Error: {resp.text}")
            return
        
        data = resp.json()
        print(f"✅ Agent Response:")
        print(f"   Status: {data['status']}")
        print(f"   Response: {data['response']}")
        print(f"   Actions: {len(data['actions_taken'])}")
        
        for action in data['actions_taken']:
            print(f"      - {action['tool']}: {action['status']}")
            if action['tool'] == 'add_task' and 'result' in action:
                print(f"        Task: {action['result'].get('title', 'N/A')}")
        
        print("\n✅ SUCCESS! Agent is working correctly!")
        print(f"\nYou can now use the frontend with:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
    except requests.Timeout:
        print(f"❌ Request timed out after 60 seconds")
        print("\nPossible issues:")
        print("   1. OpenAI API key is invalid")
        print("   2. Network/firewall blocking OpenAI")
        print("   3. OpenAI API is slow/down")
        print("\nCheck backend terminal for detailed error logs")
        
    except Exception as e:
        print(f"❌ Agent error: {e}")
        print("\nCheck backend terminal for detailed error logs")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_agent()
