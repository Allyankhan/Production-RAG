from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from app.config import settings
from app.api import chat
from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.core.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):

    await FastAPILimiter.init(redis_client)

    yield

    await redis_client.close()


app = FastAPI(
    title=settings.APP_NAME,
    description="Production RAG",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(auth_router)
app.include_router(documents_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}