from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://insighthub:insighthub@localhost:5432/insighthub"

    class Config:
        env_file = ".env"


settings = Settings()
