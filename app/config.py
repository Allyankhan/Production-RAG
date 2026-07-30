import os
from dotenv import load_dotenv

# Load variables from .env into system environment
load_dotenv()

class Settings:
    APP_NAME: str = "Production RAG"
    
    # 1. Fetch values
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "production_rag")
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "true")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SUPABASE_BUCKET:str =os.getenv("SUPABASE_BUCKET")
    SUPABASE_SERVICE_KEY: str=os.getenv("SUPABASE_SERVICE_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    REDIS_URL: str=os.getenv("REDIS_URL")
    SUPABASE_URL:str=os.getenv("SUPABASE_URL")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

    def __init__(self):
        # 2. Push values back to os.environ so LangChain can see them
        os.environ["LANGCHAIN_TRACING_V2"] = self.LANGCHAIN_TRACING_V2
        os.environ["LANGCHAIN_PROJECT"] = self.LANGCHAIN_PROJECT
        if self.LANGCHAIN_API_KEY:
            os.environ["LANGCHAIN_API_KEY"] = self.LANGCHAIN_API_KEY
        if self.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

settings = Settings()