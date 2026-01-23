from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Logistic Route Planner"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # API
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
