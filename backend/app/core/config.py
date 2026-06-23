from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

    REPOSITORY_PATH = PROJECT_ROOT / "repositories"

    CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"

    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "qwen2.5-coder:3b"
    )


settings = Settings()