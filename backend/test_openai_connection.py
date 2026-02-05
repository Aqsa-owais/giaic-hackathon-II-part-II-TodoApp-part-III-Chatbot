"""
Test OpenAI API connection directly
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

async def test_openai():
    """Test OpenAI API"""
    from openai import AsyncOpenAI
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("=" * 70)
    print("🔑 OpenAI API Connection Test")
    print("=" * 70)
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file!")
        return False
    
    print(f"\n✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
    print(f"   Length: {len(api_key)} characters")
    
    # Test connection
    print("\n🔄 Testing OpenAI API connection...")
    print("   Model: gpt-4o-mini")
    print("   Timeout: 15 seconds")
    print("   Please wait...\n")
    
    try:
        client = AsyncOpenAI(api_key=api_key, timeout=15.0, max_retries=0)
        
        start = asyncio.get_event_loop().time()
        
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'test' in one word"}
                ],
                max_tokens=5
            ),
            timeout=15.0
        )
        
        elapsed = asyncio.get_event_loop().time() - start
        
        print(f"✅ SUCCESS! OpenAI API is working!")
        print(f"   Response time: {elapsed:.2f}s")
        print(f"   Response: {response.choices[0].message.content}")
        print(f"\n✅ Your agent should work fine!")
        return True
        
    except asyncio.TimeoutError:
        print("❌ TIMEOUT! OpenAI API took more than 15 seconds")
        print("\nPossible issues:")
        print("   1. Slow internet connection")
        print("   2. OpenAI API is experiencing high load")
        print("   3. Firewall/proxy blocking OpenAI")
        print("\nTry again in a few moments.")
        return False
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERROR: {type(e).__name__}")
        print(f"   {error_msg}")
        
        if "invalid_api_key" in error_msg.lower() or "incorrect api key" in error_msg.lower():
            print("\n⚠️  Your API key appears to be invalid!")
            print("   1. Go to https://platform.openai.com/api-keys")
            print("   2. Create a new API key")
            print("   3. Update backend/.env file")
        elif "insufficient_quota" in error_msg.lower():
            print("\n⚠️  Your OpenAI account has no credits!")
            print("   1. Go to https://platform.openai.com/account/billing")
            print("   2. Add credits to your account")
        else:
            print("\n⚠️  Unexpected error - check your network connection")
        
        return False
    
    finally:
        print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        result = asyncio.run(test_openai())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
        sys.exit(1)
