"""Quick OpenAI API test"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("=" * 60)
print("OpenAI API Key Check")
print("=" * 60)

if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file")
else:
    print(f"✓ API Key found")
    print(f"  Length: {len(api_key)} characters")
    print(f"  Starts with: {api_key[:7]}...")
    print(f"  Format looks valid: {api_key.startswith('sk-')}")
    
    # Try to import openai
    try:
        import openai
        print(f"✓ OpenAI package version: {openai.__version__}")
    except ImportError as e:
        print(f"❌ OpenAI package not installed: {e}")
    
    # Try a simple sync call
    print("\nTesting API connection (this may take a few seconds)...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, timeout=10.0)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'test' in one word"}],
            max_tokens=5
        )
        
        print(f"✓ API call successful!")
        print(f"  Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ API call failed: {type(e).__name__}")
        print(f"  Error: {str(e)}")

print("=" * 60)
