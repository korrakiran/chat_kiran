from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    SARVAM_API_KEY: str = ""

    model_config = {
        "env_file": str(Path(__file__).resolve().parents[3] / "backend" / ".env"),
        "env_file_encoding": "utf-8"
    }

settings = Settings()
