from pydantic_settings import BaseSettings
from pathlib import Path

# BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = "postgresql+asyncpg://postgres:1488@localhost/sqlalchemy_tuts"
    # db_echo: bool = False
    db_echo: bool = True


setting = Settings()
