import hashlib
import hmac
from functools import lru_cache

from app.config import get_settings

def verify_signature(raw_body: bytes, signature_header: str | None) -> bool:
    
    if not signature_header:
        return False
    
    settings = get_settings()
    sig_expected = hmac.new(key=settings.APP_SECRET.encode(), msg=raw_body, digestmode=hashlib.sha256).hexdigest()

    sig_provided = signature_header.removeprefix("sha256=")

    return hmac.compare_digest(sig_expected, sig_provided)