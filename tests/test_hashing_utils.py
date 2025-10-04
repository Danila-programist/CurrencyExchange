import pytest
from app.utils.hashing import hash_password, is_verify_password


class TestHashingUtils:
    """Тесты для утилит хэширования паролей"""

    def test_hash_password(self):
        """Тест хэширования пароля"""
        password = "test_password_123"
        
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt hash format

    def test_hash_password_different_passwords(self):
        """Тест что разные пароли дают разные хэши"""
        password1 = "password1"
        password2 = "password2"
        
        hashed1 = hash_password(password1)
        hashed2 = hash_password(password2)
        
        assert hashed1 != hashed2

    def test_hash_password_same_password_different_hashes(self):
        """Тест что один пароль дает разные хэши при каждом вызове (из-за соли)"""
        password = "same_password"
        
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)
        
        assert hashed1 != hashed2

    def test_verify_password_correct(self):
        """Тест верификации правильного пароля"""
        password = "correct_password"
        hashed = hash_password(password)
        
        result = is_verify_password(password, hashed)
        
        assert result is True

    def test_verify_password_incorrect(self):
        """Тест верификации неправильного пароля"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        result = is_verify_password(wrong_password, hashed)
        
        assert result is False

    def test_verify_password_empty_password(self):
        """Тест верификации пустого пароля"""
        password = ""
        hashed = hash_password(password)
        
        result = is_verify_password(password, hashed)
        
        assert result is True

    def test_verify_password_special_characters(self):
        """Тест хэширования и верификации пароля со специальными символами"""
        password = "p@ssw0rd!#$%^&*()"
        hashed = hash_password(password)
        
        result = is_verify_password(password, hashed)
        
        assert result is True

    def test_verify_password_unicode(self):
        """Тест хэширования и верификации пароля с unicode символами"""
        password = "пароль123🔐"
        hashed = hash_password(password)
        
        result = is_verify_password(password, hashed)
        
        assert result is True