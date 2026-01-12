import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    PROJECT_NAME = "Sentinel"
    ENV = os.getenv("ENV", "dev")

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX", "sentinel-vendors") 

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

settings = Settings()
