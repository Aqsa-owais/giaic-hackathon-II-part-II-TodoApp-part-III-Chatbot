"""
Health check and diagnostic endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
from openai import AsyncOpenAI
from ..config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    message: str
    openai_configured: bool
    openai_working: bool = False


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check"""
    return HealthResponse(
        status="ok",
        message="Backend is running",
        openai_configured=bool(settings.openai_api_key)
    )


@router.get("/health/openai", response_model=HealthResponse)
async def openai_health_check():
    """Check if OpenAI API is working"""
    
    if not settings.openai_api_key:
        return HealthResponse(
            status="error",
            message="OpenAI API key not configured",
            openai_configured=False,
            openai_working=False
        )
    
    try:
        # Quick test call to OpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=10.0)
        
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            ),
            timeout=15.0
        )
        
        return HealthResponse(
            status="ok",
            message="OpenAI API is working correctly",
            openai_configured=True,
            openai_working=True
        )
        
    except asyncio.TimeoutError:
        return HealthResponse(
            status="error",
            message="OpenAI API timeout - network or API issues",
            openai_configured=True,
            openai_working=False
        )
    except Exception as e:
        return HealthResponse(
            status="error",
            message=f"OpenAI API error: {str(e)}",
            openai_configured=True,
            openai_working=False
        )
