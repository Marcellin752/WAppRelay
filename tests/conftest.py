import pytest

from app.config import get_settings


@pytest.fixture(autouse=True)
def settings_env(monkeypatch):
    """Env de test isolé du .env de dev."""
    monkeypatch.setenv("VERIFY_TOKEN", "test_verify_token")
    monkeypatch.setenv("APP_SECRET", "test_app_secret")
    monkeypatch.setenv("ACCESS_TOKEN", "test_access_token")
    monkeypatch.setenv("PHONE_NUMBER_ID", "123456789")
    
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()s