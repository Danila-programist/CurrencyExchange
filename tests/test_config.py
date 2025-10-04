from unittest.mock import patch
from app.core.config import Settings


class TestSettings:
    """Тесты для конфигурации приложения"""

    @patch.dict('os.environ', {
        'CURRENCY_API_KEY': 'test_api_key',
        'BASE_URL': 'https://api.test.com',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_CONTAINER_NAME': 'test_container',
        'DB_PORT': '5432',
        'DB': 'postgresql',
        'PWD_ALGORYTHM': 'bcrypt',
        'ALGORYTHM': 'HS256',
        'SECRET': 'test_secret_key',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'REDIS_CONTAINER_NAME': 'redis_container',
        'REDIS_URL': 'redis://localhost:6379'
    })
    def test_settings_initialization(self):
        """Тест инициализации настроек с переменными окружения"""
        settings = Settings()
        
        assert settings.CURRENCY_API_KEY == 'test_api_key'
        assert str(settings.BASE_URL) == 'https://api.test.com'
        assert settings.DB_NAME == 'test_db'
        assert settings.DB_USER == 'test_user'
        assert settings.DB_PASSWORD == 'test_password'
        assert settings.DB_HOST == 'localhost'
        assert settings.DB_CONTAINER_NAME == 'test_container'
        assert settings.DB_PORT == 5432
        assert settings.DB == 'postgresql'
        assert settings.PWD_ALGORYTHM == 'bcrypt'
        assert settings.ALGORYTHM == 'HS256'
        assert settings.SECRET == 'test_secret_key'
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert settings.REDIS_CONTAINER_NAME == 'redis_container'
        assert settings.REDIS_URL == 'redis://localhost:6379'

    @patch.dict('os.environ', {
        'CURRENCY_API_KEY': 'test_api_key',
        'BASE_URL': 'https://api.test.com',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_CONTAINER_NAME': 'test_container',
        'DB_PORT': '5432',
        'DB': 'postgresql',
        'PWD_ALGORYTHM': 'bcrypt',
        'ALGORYTHM': 'HS256',
        'SECRET': 'test_secret_key',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'REDIS_CONTAINER_NAME': 'redis_container',
        'REDIS_URL': 'redis://localhost:6379'
    })
    def test_async_database_dsn_property(self):
        """Тест свойства ASYNC_DATABASE_DSN"""
        settings = Settings()
        
        expected_dsn = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
        assert settings.ASYNC_DATABASE_DSN == expected_dsn

    @patch.dict('os.environ', {
        'CURRENCY_API_KEY': 'test_api_key',
        'BASE_URL': 'https://api.test.com',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_CONTAINER_NAME': 'test_container',
        'DB_PORT': '5432',
        'DB': 'postgresql',
        'PWD_ALGORYTHM': 'bcrypt',
        'ALGORYTHM': 'HS256',
        'SECRET': 'test_secret_key',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'REDIS_CONTAINER_NAME': 'redis_container',
        'REDIS_URL': 'redis://localhost:6379'
    })
    def test_database_dsn_with_special_characters(self):
        """Тест DSN с специальными символами в пароле"""
        with patch.dict('os.environ', {'DB_PASSWORD': 'p@ssw0rd!@#'}):
            settings = Settings()
            
            expected_dsn = "postgresql+asyncpg://test_user:p%40ssw0rd%21%40%23@localhost:5432/test_db"
            assert settings.ASYNC_DATABASE_DSN == expected_dsn

    def test_settings_missing_required_field(self):
        """Тест ошибки при отсутствии обязательного поля"""
        with patch.dict('os.environ', {}, clear=True):
            try:
                Settings()
                assert False, "Expected ValidationError"
            except Exception:
                # Ожидаем ошибку валидации Pydantic
                pass

    @patch.dict('os.environ', {
        'CURRENCY_API_KEY': 'test_api_key',
        'BASE_URL': 'https://api.test.com',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_CONTAINER_NAME': 'test_container',
        'DB_PORT': '5432',
        'DB': 'postgresql',
        'PWD_ALGORYTHM': 'bcrypt',
        'ALGORYTHM': 'HS256',
        'SECRET': 'test_secret_key',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'REDIS_CONTAINER_NAME': 'redis_container',
        'REDIS_URL': 'redis://localhost:6379'
    })
    def test_settings_invalid_url(self):
        """Тест ошибки при неверном URL"""
        with patch.dict('os.environ', {'BASE_URL': 'invalid-url'}):
            try:
                Settings()
                assert False, "Expected ValidationError"
            except Exception:
                # Ожидаем ошибку валидации Pydantic
                pass

    @patch.dict('os.environ', {
        'CURRENCY_API_KEY': 'test_api_key',
        'BASE_URL': 'https://api.test.com',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_CONTAINER_NAME': 'test_container',
        'DB_PORT': '5432',
        'DB': 'postgresql',
        'PWD_ALGORYTHM': 'bcrypt',
        'ALGORYTHM': 'HS256',
        'SECRET': 'test_secret_key',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'REDIS_CONTAINER_NAME': 'redis_container',
        'REDIS_URL': 'redis://localhost:6379'
    })
    def test_settings_invalid_port(self):
        """Тест ошибки при неверном порте"""
        with patch.dict('os.environ', {'DB_PORT': 'invalid_port'}):
            try:
                Settings()
                assert False, "Expected ValidationError"
            except Exception:
                # Ожидаем ошибку валидации Pydantic
                pass

    @patch.dict('os.environ', {
        'CURRENCY_API_KEY': 'test_api_key',
        'BASE_URL': 'https://api.test.com',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_CONTAINER_NAME': 'test_container',
        'DB_PORT': '5432',
        'DB': 'postgresql',
        'PWD_ALGORYTHM': 'bcrypt',
        'ALGORYTHM': 'HS256',
        'SECRET': 'test_secret_key',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'REDIS_CONTAINER_NAME': 'redis_container',
        'REDIS_URL': 'redis://localhost:6379'
    })
    def test_settings_model_config(self):
        """Тест конфигурации модели"""
        settings = Settings()
        
        # Проверяем что модель настроена правильно
        assert hasattr(settings, 'model_config')
        assert settings.model_config is not None