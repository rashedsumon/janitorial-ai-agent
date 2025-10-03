# src/whatsapp.py
from twilio.rest import Client
from .config import settings
from loguru import logger

class WhatsAppClient:
    def __init__(self, account_sid=None, auth_token=None, whatsapp_from=None):
        self.account_sid = account_sid or settings.TWILIO_ACCOUNT_SID
        self.auth_token = auth_token or settings.TWILIO_AUTH_TOKEN
        self.whatsapp_from = whatsapp_from or settings.TWILIO_WHATSAPP_FROM
        if not (self.account_sid and self.auth_token and self.whatsapp_from):
            logger.warning("Twilio credentials not fully configured. WhatsApp messages won't be sent.")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to_whatsapp_number: str, body: str):
        if not self.client:
            logger.info(f"[DEMO] WhatsApp to {to_whatsapp_number}: {body}")
            return {"status": "demo", "to": to_whatsapp_number, "body": body}
        msg = self.client.messages.create(
            body=body,
            from_=self.whatsapp_from,
            to=f"whatsapp:{to_whatsapp_number}"
        )
        logger.info(f"Sent message SID: {msg.sid}")
        return {"status": "sent", "sid": msg.sid}
