from fastapi import APIRouter, Request, Response, Query, HTTPException, BackgroundTasks
import json
from app.config import get_settings
from app.core.security import verify_signature
from app.services.message_parser import extract_messages
from app.services.message_forwarder import MessageForwarder

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str | None = Query(None, alias="hub.mode"),
    hub_verify_token: str | None = Query(None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(None, alias="hub.challenge")
):
    """Hanshake"""

    settings = get_settings()
    if hub_mode == "subscribe" and hub_verify_token == settings.VERIFY_TOKEN:
        if hub_challenge is None:
            raise HTTPException(status_code=400, detail="Missing hub.challenge")
        
        # text/plain obligatoire
        return Response(content=hub_challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Invalid verification token")

@router.post("/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    """Reception of events"""
    raw_body = await request.body()
    signature = request.headers.get("x-hub-signature-256")

    if not verify_signature(raw_body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # parsing in JSON
    payload = json.loads(raw_body)

    # Extraction of entry messages
    messages = extract_messages(payload)

    for message in messages:
        background_tasks.add_task(process_message, message)

    return {"status": "received"}

_forwarder: MessageForwarder | None = None
def get_forwarder() -> MessageForwarder:
    global _forwarder
    if _forwarder is None:
        _forwarder = MessageForwarder()
    return _forwarder

async def process_message(message: dict) -> None:
    await get_forwarder().forward(message)