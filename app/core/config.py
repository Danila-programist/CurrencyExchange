from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

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
    DB: str

    model_config = SettingsConfigDict(env_file=['.env.example', '.env'], env_file_encoding='utf-8')


settings = Settings()