import httpx
from datetime import datetime, timezone
from app.config import get_settings
from app.services.whatsapp_client import WhatsAppClient

class MessageForwarder:
    def __init__(self, client: WhatsAppClient | None = None) -> None:
        self._client = client or WhatsAppClient()
        self._target = get_settings().RELAY_TARGET_NUMBER

    async def forward(self, message: dict) -> None:
        body = self._format_message(message)
        try:
            await self._client.send_text(self._target, body)
            print(f"message_forwarded: id={message.get('id')} to={self._target}")
        except httpx.HTTPError as exc:
            print(f"forward_failed: id={message.get('id')} error={exc}")

    def _format_message(self, message: dict) -> str:
        sender = message.get("from", "inconnu")
        timestamp = int(message.get("timestamp", 0))
        date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%d/%m/%Y %H:%M")

        content = message.get("text", {}).get("body", "[content no text]")

        return f"from : {sender} — {date}\n{content}"