from pydantic import BaseModel
from pydantic_settings import BaseSettings


# BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseModel):
    url: str = "postgresql+asyncpg://postgres:1488@localhost/sqlalchemy_tuts"
    echo: bool = False
    # echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()


setting = Settings()
