# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    JM_BASE_URL = os.getenv("JM_BASE_URL")
    JM_API_KEY = os.getenv("JM_API_KEY")
    GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
    DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("1","true","yes")
    KAGGLE_SAMPLE_PATH = os.getenv("KAGGLE_SAMPLE_PATH", "data/sample_hr.csv")
    SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "Asia/Dhaka")

settings = Settings()
