import os
from pathlib import Path

from pydantic_settings import BaseSettings

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    # postgres settings
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    # auth settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # S3 settings
    BUCKET_NAME: str
    S3_HOST: str
    S3_PORT: str
    S3_USER: str
    S3_PASSWORD: str
    # RabbitMQ settings
    # MQ_USER:str
    # MQ_PASSWORD:str
    # AQMP_PORT:int
    # INTF_PORT:int
    # MQ_HOST:str
    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", ".env"
        )


settings = Settings()
