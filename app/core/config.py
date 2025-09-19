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
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=str(self.DB_PORT),
            path=f"/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=['.env.example', '.env'], env_file_encoding='utf-8')


settings = Settings()