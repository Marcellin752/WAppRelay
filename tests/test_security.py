import hashlib
import hmac

from app.core.security import verify_signature


def _sign(body: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def test_valid_signature():
    body = b'{"entry": []}'
    assert verify_signature(body, _sign(body, "test_app_secret")) is True


def test_tampered_body():
    body = b'{"entry": []}'
    assert verify_signature(b'{"entry": [1]}', _sign(body, "test_app_secret")) is False


def test_wrong_secret():
    body = b'{"entry": []}'
    assert verify_signature(body, _sign(body, "autre_secret")) is False


def test_missing_header():
    assert verify_signature(b'{}', None) is False


def test_invalid_header_format():
    body = b'{}'
    assert verify_signature(body, "not-a-signature") is False
