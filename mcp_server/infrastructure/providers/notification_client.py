from typing import Optional
import requests
from fastapi import HTTPException
from ...config import get_settings
from ...core.services import INotificationClient

settings = get_settings()


class HttpNotificationClient(INotificationClient):
    def send(self, to: str, channel: str, subject: Optional[str], message: str) -> None:
        url = f"{settings.NOTIFY_URL}/send"
        payload = {
            "to": to,
            "channel": channel,
            "subject": subject,
            "message": message,
        }
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Notification failed: {r.text}")
