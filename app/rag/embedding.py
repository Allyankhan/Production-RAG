from langchain_openai import OpenAIEmbeddings
from app.config import settings

embeddings=OpenAIEmbeddings(
    model='text-embedding-3-small',
    api_key=settings.OPENAI_API_KEY
)