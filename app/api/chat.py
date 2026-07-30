import os
from fastapi import APIRouter, HTTPException
from langsmith import traceable
from fastapi import Request

from app.models.schemas import ChatRequest, ChatResponse
from app.graph.graph import graph
from app.logging.logger import logger
from app.cache.redis_client import redis_client
from app.cache.cache import get_cache_key
from app.security.inputguard import is_prompt_injection
from app.security.llm_guard import check_prompt_security
from fastapi import Depends
from fastapi_limiter.depends import RateLimiter
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()


os.environ['LANGSMITH_TRACING'] = "true"
@router.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[
        Depends(RateLimiter(times=5, seconds=60))
    ]
)
@traceable(name="EndPoint")
async def chat(
    request: Request,
    payload: ChatRequest
    
):
    
    logger.info(f"Question: {payload.question}")
    question = payload.question
    # 2. Cache Check
    cache_key = get_cache_key(question)
    cached = redis_client.get(cache_key)

    if cached:
        return {
            "answer": cached, 
            "cached": True
        }
    
    # 1. Security Check
    if is_prompt_injection(question):
        raise HTTPException(
            status_code=400,
            detail="Possible SECURITY attack blocked by system" 
        )
    if not check_prompt_security(payload.question):
        raise HTTPException(
        status_code=400,
        detail="system blocked unsafe prompt."
    )

    

    # 3. Graph Invocation
    result = graph.invoke(
        {
            "question": question
        }
    )

    # 4. Set Cache
    redis_client.set(
        cache_key,
        result["answer"],
        ex=3600
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }