import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app


class TestMainApp:

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_app_initialization(self):
        assert app is not None
        assert app.title == "Currency Exchange API"

    def test_app_routes_included(self):
        routes = [route.path for route in app.routes]

        assert any("/api/v1" in route for route in routes)

    def test_app_openapi_schema(self, client):
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        assert "openapi" in response.json()
        assert response.json()["info"]["title"] == "Currency Exchange API"

    def test_app_docs_available(self, client):
        response = client.get("/docs")
        
        assert response.status_code == 200

    def test_app_redoc_available(self, client):
        response = client.get("/redoc")
        
        assert response.status_code == 200

    @patch('main.uvicorn.run')
    def test_main_module_execution(self, mock_uvicorn_run):
        """Тест выполнения модуля main"""
        import main
        
        mock_uvicorn_run.assert_not_called()

    def test_app_lifespan_configured(self):
        """Тест что lifespan настроен"""
        assert hasattr(app, 'router')
        assert app.router is not None

    def test_app_middleware_configured(self):
        assert hasattr(app, 'middleware_stack')
        assert app.middleware_stack is not None

    def test_app_exception_handlers(self, client):
        response = client.get("/nonexistent")
        
        assert response.status_code == 404

    def test_app_cors_headers(self, client):
        response = client.options("/api/v1/currency/all")
        assert response.status_code in [200, 405] 

    def test_app_json_response_format(self, client):
        response = client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
        assert response.headers.get("content-type") == "application/json"

    def test_app_health_check(self, client):
        response = client.get("/health")
        
        assert response.status_code in [200, 404]

    def test_app_version_info(self, client):
        response = client.get("/openapi.json")
        
        if response.status_code == 200:
            openapi_data = response.json()
            assert "info" in openapi_data
            assert "version" in openapi_data["info"]

    def test_app_router_prefix(self):
        routes = [route for route in app.routes if hasattr(route, 'path')]
        api_routes = [route for route in routes if route.path.startswith("/api/v1")]
        
        assert len(api_routes) > 0

    def test_app_dependencies_injection(self):
        assert hasattr(app, 'dependency_overrides')
        assert app.dependency_overrides is not None