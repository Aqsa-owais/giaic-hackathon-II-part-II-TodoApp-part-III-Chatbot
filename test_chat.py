import requests
import json
import uuid

# Generate unique email
unique_email = f'test{uuid.uuid4().hex[:8]}@example.com'

# Register user
try:
    response = requests.post('http://localhost:8000/api/register', 
                           json={'email': unique_email, 'password': 'TestPassword123!'})
    print('Register response:', response.status_code, response.text)
    
    if response.status_code == 201:
        user_data = response.json()
        user_id = user_data.get('id')
        print('User registered successfully! User ID:', user_id)
        
        # Login user
        login_response = requests.post('http://localhost:8000/api/login', 
                               json={'email': unique_email, 'password': 'TestPassword123!'})
        print('Login response:', login_response.status_code, login_response.text)
        
        if login_response.status_code == 200:
            data = login_response.json()
            token = data.get('access_token')
            print('Token:', token[:20] + '...' if token else 'None')
            
            # Test chat API - Create task through AI agent
            if token and user_id:
                print(f'Testing AI agent with user ID: {user_id}')
                chat_response = requests.post(f'http://localhost:8000/api/v1/users/{user_id}/chat',
                                            headers={'Authorization': f'Bearer {token}'},
                                            json={'message': 'Create a task to buy groceries for dinner tonight'})
                print('Chat response:', chat_response.status_code)
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    print('AI Response:', chat_data.get('response'))
                    print('Actions taken:', chat_data.get('actions_taken'))
                else:
                    print('Chat error:', chat_response.text)
        
except Exception as e:
    print('Error:', e)