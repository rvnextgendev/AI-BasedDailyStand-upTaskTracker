import os
from functools import lru_cache


class Settings:
    # Database
    DB_HOST: str = os.getenv("DB_HOST", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "standupdb")
    DB_USER: str = os.getenv("DB_USER", "standupuser")
    DB_PASS: str = os.getenv("DB_PASS", "standuppass")

    # Local service URLs
    ML_URL: str = os.getenv("ML_URL", "http://ml-service:8000")
    NOTIFY_URL: str = os.getenv("NOTIFY_URL", "http://notification-service:8000")

    # JWT / Auth
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_PUBLIC_KEY: str = os.getenv("JWT_PUBLIC_KEY", "")
    JWT_PUBLIC_KEY_PATH: str = os.getenv("JWT_PUBLIC_KEY_PATH", "/keys/jwt.pub")

    # Provider switches
    ML_PROVIDER: str = os.getenv("ML_PROVIDER", "LOCAL")  # LOCAL | AZURE | BEDROCK | GCP
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "LOCAL")  # LOCAL | AZURE | BEDROCK | GCP

    # Azure AI / Azure OpenAI
    AZURE_ML_ENDPOINT: str = os.getenv("AZURE_ML_ENDPOINT", "")
    AZURE_ML_API_KEY: str = os.getenv("AZURE_ML_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")

    # AWS Bedrock
    BEDROCK_REGION: str = os.getenv("BEDROCK_REGION", "")
    BEDROCK_ACCESS_KEY: str = os.getenv("BEDROCK_ACCESS_KEY", "")
    BEDROCK_SECRET_KEY: str = os.getenv("BEDROCK_SECRET_KEY", "")

    # Google Vertex AI
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    GCP_MODEL_NAME: str = os.getenv("GCP_MODEL_NAME", "")

    # Local LLM (Ollama)
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://llm-service:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")

    # OpenAI (optional non-Azure)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()
