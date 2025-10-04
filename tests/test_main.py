"""
Простой тест для проверки что основное приложение импортируется корректно
"""

import pytest

from main import app


def test_main_app_import():
    """Тест что основное приложение импортируется без ошибок"""
    assert app is not None
    assert hasattr(app, 'title')
    assert app.title == "Currency Exchange API"


def test_main_app_routes():
    """Тест что у приложения есть роуты"""
    assert hasattr(app, 'routes')
    assert len(app.routes) > 0


def test_main_app_router():
    """Тест что у приложения есть роутер"""
    assert hasattr(app, 'router')
    assert app.router is not None
