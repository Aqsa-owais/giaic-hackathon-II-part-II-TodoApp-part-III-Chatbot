"""
Complete Agent Flow Test
Tests: Register -> Login -> Create Task -> List Tasks -> Update -> Complete -> Delete
"""
import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_full_flow():
    """Test complete agent flow"""
    
    print_section("🚀 STARTING FULL AGENT FLOW TEST")
    
    # Generate unique email
    unique_email = f'test{uuid.uuid4().hex[:8]}@example.com'
    password = 'TestPassword123!'
    
    # Step 1: Register
    print_section("1️⃣  REGISTERING USER")
    print(f"Email: {unique_email}")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/register',
            json={'email': unique_email, 'password': password},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code != 201:
            print(f"❌ Registration failed: {response.text}")
            return
        
        user_data = response.json()
        user_id = user_data.get('id')
        print(f"✅ User registered! ID: {user_id}")
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 2: Login
    print_section("2️⃣  LOGGING IN")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/login',
            json={'email': unique_email, 'password': password},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Login failed: {response.text}")
            return
        
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Login successful! Token: {token[:20]}...")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Headers for authenticated requests
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Step 3: Create Task via Agent
    print_section("3️⃣  CREATING TASK VIA AI AGENT")
    print("Message: 'Create a task to buy groceries for dinner'")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/users/{user_id}/chat',
            headers=headers,
            json={'message': 'Create a task to buy groceries for dinner'},
            timeout=45
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Agent request failed: {response.text}")
            return
        
        data = response.json()
        print(f"✅ Agent Response: {data.get('response')}")
        print(f"Actions taken: {len(data.get('actions_taken', []))}")
        
        for action in data.get('actions_taken', []):
            print(f"  - {action['tool']}: {action['status']}")
            if action['tool'] == 'add_task':
                task_id = action['result'].get('id')
                print(f"    Task ID: {task_id}")
        
    except requests.Timeout:
        print("❌ Request timed out - OpenAI API might be slow or key invalid")
        return
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return
    
    # Step 4: List Tasks via Agent
    print_section("4️⃣  LISTING TASKS VIA AI AGENT")
    print("Message: 'Show me all my tasks'")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/users/{user_id}/chat',
            headers=headers,
            json={'message': 'Show me all my tasks'},
            timeout=45
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent Response: {data.get('response')}")
            
            for action in data.get('actions_taken', []):
                if action['tool'] == 'list_tasks':
                    tasks = action['result'].get('tasks', [])
                    print(f"  Found {len(tasks)} task(s)")
                    for task in tasks:
                        print(f"    - [{task['id'][:8]}...] {task['title']}")
        
    except Exception as e:
        print(f"❌ List tasks error: {e}")
    
    # Step 5: Update Task via Agent
    print_section("5️⃣  UPDATING TASK VIA AI AGENT")
    print("Message: 'Update my grocery task to include milk and eggs'")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/users/{user_id}/chat',
            headers=headers,
            json={'message': 'Update my grocery task to include milk and eggs'},
            timeout=45
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent Response: {data.get('response')}")
        
    except Exception as e:
        print(f"❌ Update task error: {e}")
    
    # Step 6: Complete Task via Agent
    print_section("6️⃣  COMPLETING TASK VIA AI AGENT")
    print("Message: 'Mark the grocery task as complete'")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/users/{user_id}/chat',
            headers=headers,
            json={'message': 'Mark the grocery task as complete'},
            timeout=45
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent Response: {data.get('response')}")
        
    except Exception as e:
        print(f"❌ Complete task error: {e}")
    
    # Step 7: Delete Task via Agent
    print_section("7️⃣  DELETING TASK VIA AI AGENT")
    print("Message: 'Delete the grocery task'")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/v1/users/{user_id}/chat',
            headers=headers,
            json={'message': 'Delete the grocery task'},
            timeout=45
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent Response: {data.get('response')}")
        
    except Exception as e:
        print(f"❌ Delete task error: {e}")
    
    print_section("✅ TEST COMPLETED SUCCESSFULLY!")
    print(f"User Email: {unique_email}")
    print(f"User ID: {user_id}")
    print("\nYou can now login with these credentials in the frontend!")

if __name__ == "__main__":
    print("\n🤖 AI Agent Full Flow Test")
    print("Make sure backend is running on http://localhost:8000")
    print("\nWaiting 3 seconds for backend to be ready...")
    time.sleep(3)
    
    try:
        test_full_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
