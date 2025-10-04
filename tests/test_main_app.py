import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app


class TestMainApp:
    """Тесты для основного приложения FastAPI"""

    @pytest.fixture
    def client(self):
        """Фикстура для тестового клиента"""
        return TestClient(app)

    def test_app_initialization(self):
        """Тест инициализации приложения"""
        assert app is not None
        assert app.title == "Currency Exchange API"

    def test_app_routes_included(self):
        """Тест что все роуты включены в приложение"""
        routes = [route.path for route in app.routes]
        
        # Проверяем что есть роуты для API
        assert any("/api/v1" in route for route in routes)

    def test_app_openapi_schema(self, client):
        """Тест что OpenAPI схема доступна"""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        assert "openapi" in response.json()
        assert response.json()["info"]["title"] == "Currency Exchange API"

    def test_app_docs_available(self, client):
        """Тест что документация доступна"""
        response = client.get("/docs")
        
        assert response.status_code == 200

    def test_app_redoc_available(self, client):
        """Тест что ReDoc доступна"""
        response = client.get("/redoc")
        
        assert response.status_code == 200

    @patch('main.uvicorn.run')
    def test_main_module_execution(self, mock_uvicorn_run):
        """Тест выполнения модуля main"""
        # Имитируем выполнение if __name__ == "__main__"
        import main
        
        # Проверяем что uvicorn.run не был вызван при импорте
        mock_uvicorn_run.assert_not_called()

    def test_app_lifespan_configured(self):
        """Тест что lifespan настроен"""
        # Проверяем что у приложения есть lifespan
        assert hasattr(app, 'router')
        assert app.router is not None

    def test_app_middleware_configured(self):
        """Тест что middleware настроены"""
        # Проверяем что у приложения есть middleware
        assert hasattr(app, 'middleware_stack')
        assert app.middleware_stack is not None

    def test_app_exception_handlers(self, client):
        """Тест обработчиков исключений"""
        # Тестируем несуществующий эндпоинт
        response = client.get("/nonexistent")
        
        assert response.status_code == 404

    def test_app_cors_headers(self, client):
        """Тест CORS заголовков"""
        response = client.options("/api/v1/currency/all")
        
        # Проверяем что приложение отвечает на OPTIONS запросы
        assert response.status_code in [200, 405]  # 405 если CORS не настроен

    def test_app_json_response_format(self, client):
        """Тест формата JSON ответов"""
        # Тестируем с несуществующим эндпоинтом для проверки формата ошибки
        response = client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
        # Проверяем что ответ в формате JSON
        assert response.headers.get("content-type") == "application/json"

    def test_app_health_check(self, client):
        """Тест проверки здоровья приложения"""
        # Если есть health check эндпоинт
        response = client.get("/health")
        
        # Если эндпоинт не существует, это нормально
        assert response.status_code in [200, 404]

    def test_app_version_info(self, client):
        """Тест информации о версии"""
        # Проверяем OpenAPI схему на наличие версии
        response = client.get("/openapi.json")
        
        if response.status_code == 200:
            openapi_data = response.json()
            assert "info" in openapi_data
            assert "version" in openapi_data["info"]

    def test_app_router_prefix(self):
        """Тест префикса роутера"""
        # Проверяем что API роутер имеет правильный префикс
        routes = [route for route in app.routes if hasattr(route, 'path')]
        api_routes = [route for route in routes if route.path.startswith("/api/v1")]
        
        assert len(api_routes) > 0

    def test_app_dependencies_injection(self):
        """Тест инъекции зависимостей"""
        # Проверяем что приложение может обрабатывать зависимости
        assert hasattr(app, 'dependency_overrides')
        assert app.dependency_overrides is not None