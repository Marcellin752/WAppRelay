import hashlib
import hmac

from fastapi.testclient import TestClient

from app.main import app

# TestClient est le moyen de tester FastAPI simulant un vrai client
client = TestClient(app)

APP_SECRET = "test_app_secret"
VERIFY_TOKEN = "test_verify_token"


def _sign(body: bytes) -> str:
    """Reproduire la signature que Meta enverrait."""
    return "sha256=" + hmac.new(APP_SECRET.encode(), body, hashlib.sha256).hexdigest()


def test_verify_webhook_success():
    """rendre le challenge brut."""
    response = client.get(
        "/webhook",
        params={"hub.mode": "subscribe", "hub.verify_token": VERIFY_TOKEN,
                "hub.challenge": "1234567890"},
    )
    assert response.status_code == 200
    assert response.text == "1234567890"
    assert response.headers["content-type"].startswith("text/plain")


def test_verify_webhook_invalid_token():
    """Handshake avec un mauvais token"""
    response = client.get(
        "/webhook",
        params={"hub.mode": "subscribe", "hub.verify_token": "mauvais",
                "hub.challenge": "1234567890"},
    )
    assert response.status_code == 403


def test_verify_webhook_missing_challenge():
    """Bon token mais challenge absent"""
    response = client.get(
        "/webhook",
        params={"hub.mode": "subscribe", "hub.verify_token": VERIFY_TOKEN},
    )
    assert response.status_code == 400


def test_post_webhook_valid_signature():
    """POST signé correctement"""
    body = b'{"object": "whatsapp_business_account", "entry": []}'
    response = client.post(
        "/webhook",
        content=body,
        headers={"x-hub-signature-256": _sign(body)},
    )
    assert response.status_code == 200
    assert response.json() == {"status": "received"}


def test_post_webhook_invalid_signature():
    """POST avec un body modifié."""
    body = b'{"object": "whatsapp_business_account", "entry": []}'
    response = client.post(
        "/webhook",
        content=body,
        headers={"x-hub-signature-256": _sign(b"contenu_modifie")},
    )
    assert response.status_code == 403


def test_post_webhook_missing_signature():
    """POST sans signature."""
    response = client.post(
        "/webhook",
        content=b'{"object": "whatsapp_business_account", "entry": []}',
    )
    assert response.status_code == 403