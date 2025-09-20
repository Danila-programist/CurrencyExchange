from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, PostgresDsn

class Settings(BaseSettings):
    
    # External API
    CURRENCY_API_KEY: str
    BASE_URL: AnyUrl

    # Database
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_CONTAINER_NAME: str
    DB_PORT: int
    DB: str

    @property
    def ASYNC_DATABASE_DSN(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Hashing
    PWD_ALGORYTHM: str
    ALGORYTHM: str
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Redis
    REDIS_CONTAINER_NAME: str
    REDIS_URL: str


    model_config = SettingsConfigDict(env_file=['.env.example', '.env'], env_file_encoding='utf-8')


settings = Settings()