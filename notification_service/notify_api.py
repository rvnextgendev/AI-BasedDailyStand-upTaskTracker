from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notification Service")


class Message(BaseModel):
    to: str
    channel: str  # email or whatsapp
    subject: str | None = None
    message: str
    requested_by: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/send")
def send(msg: Message):
    # Stub implementation; extend with real provider (Twilio/SendGrid/etc.)
    return {"status": "sent", "channel": msg.channel, "to": msg.to}
