import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = os.getenv("APP_NAME", "Technical Interview API")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    ollama_api_key: str | None = os.getenv("KEY_OLLAMA_MODEL")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "https://ollama.com")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
    ollama_timeout: float = float(os.getenv("OLLAMA_TIMEOUT", "60"))


settings = Settings()
