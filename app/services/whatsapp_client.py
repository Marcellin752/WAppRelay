import httpx
from app.config import get_settings

class WhatsAppClient:
    BASE_URL = "https://graph.facebook.com/v23.0"

    def __init__(self) -> None:
        settings = get_settings()
        self._token = settings.ACCESS_TOKEN
        self._phone_number_id = settings.PHONE_NUMBER_ID
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={"Authorization": f"Bearer {self._token}"},
            timeout=30.0,
        )

    async def send_text(self, to: int, body: str) -> str:
        response = await self._client.post(
            f"/{self._phone_number_id}/messages",
            json={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "text",
                "text": {"body": body},
            },
        )
        response.raise_for_status()
        return response.json()["messages"][0]["id"]

    async def close(self) -> None:
        await self._client.aclose()