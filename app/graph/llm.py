from langchain_openai import ChatOpenAI
from app.config import settings

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=settings.OPENAI_API_KEY, streaming=True)

