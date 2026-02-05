"""
Simple test script for OpenAI Agent
"""
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

from src.services.openai_agent import TaskAgent

async def test_agent():
    """Test the TaskAgent"""
    print("=" * 60)
    print("Testing OpenAI TaskAgent")
    print("=" * 60)
    
    # Create agent
    print("\n1. Initializing agent...")
    agent = TaskAgent()
    print("✓ Agent initialized successfully")
    
    # Test user ID (fake UUID for testing)
    test_user_id = "12345678-1234-1234-1234-123456789012"
    
    # Test 1: Simple greeting
    print("\n2. Testing simple message...")
    response = await agent.process_message(
        user_id=test_user_id,
        message="Hello! Can you help me manage my tasks?"
    )
    print(f"Response: {response['response']}")
    print(f"Status: {response['status']}")
    print(f"Actions: {len(response['actions_taken'])}")
    
    # Test 2: Create a task
    print("\n3. Testing task creation...")
    response = await agent.process_message(
        user_id=test_user_id,
        message="Create a task to buy groceries"
    )
    print(f"Response: {response['response']}")
    print(f"Status: {response['status']}")
    print(f"Actions taken: {len(response['actions_taken'])}")
    if response['actions_taken']:
        for action in response['actions_taken']:
            print(f"  - {action['tool']}: {action['status']}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(test_agent())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
