import asyncio
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

async def test_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key (first 20 chars): {api_key[:20] if api_key else 'NOT SET'}")
    
    client = AsyncOpenAI(api_key=api_key)
    
    try:
        print("Testing OpenAI API connection...")
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello in one word"}
                ],
                max_tokens=10,
                timeout=10.0
            ),
            timeout=15.0
        )
        
        print(f"Success! Response: {response.choices[0].message.content}")
        return True
    except asyncio.TimeoutError:
        print("ERROR: Request timed out after 15 seconds")
        return False
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_openai())
    print(f"\nTest {'PASSED' if result else 'FAILED'}")
