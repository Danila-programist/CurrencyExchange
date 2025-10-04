import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os


@pytest.fixture(scope="session")
def test_env_vars():
    """Фикстура с тестовыми переменными окружения"""
    test_env = {
        'CURRENCY_API_KEY': 'test_api_key_123',
        'BASE_URL': 'https://api.test.com',
        'DB_NAME': 'test_currency_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_CONTAINER_NAME': 'test_db_container',
        'DB_PORT': '5432',
        'DB': 'postgresql',
        'PWD_ALGORYTHM': 'bcrypt',
        'ALGORYTHM': 'HS256',
        'SECRET': 'test_secret_key_for_jwt',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'REDIS_CONTAINER_NAME': 'test_redis_container',
        'REDIS_URL': 'redis://localhost:6379'
    }
    
    with patch.dict(os.environ, test_env):
        yield test_env


@pytest.fixture
def sample_currency_rates():
    """Фикстура с примерными курсами валют"""
    return {
        "EUR": {"value": 0.85},
        "GBP": {"value": 0.73},
        "JPY": {"value": 110.0},
        "CAD": {"value": 1.25},
        "AUD": {"value": 1.35}
    }


@pytest.fixture
def sample_currency_data():
    """Фикстура с примерными данными валюты"""
    return {
        "symbol": "$",
        "name": "US Dollar",
        "symbol_native": "$",
        "decimal_digits": 2,
        "rounding": 0,
        "code": "USD",
        "name_plural": "US dollars",
        "type": "fiat",
        "countries": ["US", "EC", "SV", "MH", "FM", "PW", "TL", "ZW"]
    }


@pytest.fixture
def sample_conversion_data():
    """Фикстура с примерными данными конвертации"""
    return {
        "from_currency": "USD",
        "to_currency": "EUR",
        "rate": 0.85,
        "amount": 100.0,
        "converted_amount": 85.0
    }


@pytest.fixture
def mock_external_api_response():
    """Фикстура с мок-ответом внешнего API"""
    return {
        "data": {
            "USD": {"value": 1.0},
            "EUR": {"value": 0.85},
            "GBP": {"value": 0.73},
            "JPY": {"value": 110.0}
        },
        "meta": {
            "last_updated_at": "2024-01-01T00:00:00Z"
        }
    }


@pytest.fixture
def test_passwords():
    """Фикстура с тестовыми паролями"""
    return {
        "simple": "password123",
        "complex": "P@ssw0rd!2024",
        "unicode": "пароль123🔐",
        "empty": "",
        "special": "!@#$%^&*()_+-=[]{}|;:,.<>?"
    }
