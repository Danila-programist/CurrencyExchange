from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
    
    # External API
    CURRENCY_API_KEY: str
    BASE_URL: AnyUrl

    model_config = SettingsConfigDict(env_file=['.env.example', '.env'], env_file_encoding='utf-8')


settings = Settings()