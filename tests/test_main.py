from main import app


def test_main_app_import():
    assert app is not None
    assert hasattr(app, 'title')
    assert app.title == "Currency Exchange API"


def test_main_app_routes():
    assert hasattr(app, 'routes')
    assert len(app.routes) > 0


def test_main_app_router():
    assert hasattr(app, 'router')
    assert app.router is not None
