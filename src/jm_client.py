# src/jm_client.py
import requests
from .config import settings
from loguru import logger

class JanitorialManagerClient:
    def __init__(self, base_url=None, api_key=None, demo_mode=None):
        self.base_url = base_url or settings.JM_BASE_URL
        self.api_key = api_key or settings.JM_API_KEY
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def create_client(self, client_data: dict):
        """Create a client record in Janitorial Manager.
           In DEMO mode this logs and returns a fake response."""
        if self.demo_mode:
            logger.info(f"[DEMO] create_client called: {client_data}")
            return {"status": "ok", "id": f"demo-client-{client_data.get('name','unknown')}"}
        url = f"{self.base_url}/clients"
        resp = requests.post(url, json=client_data, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def create_time_entry(self, employee_id: str, date: str, hours: float, meta: dict = None):
        if self.demo_mode:
            logger.info(f"[DEMO] create_time_entry: emp={employee_id}, date={date}, hours={hours}")
            return {"status": "ok"}
        url = f"{self.base_url}/time_entries"
        payload = {"employee_id": employee_id, "date": date, "hours": hours, "meta": meta or {}}
        resp = requests.post(url, json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_client(self, client_id):
        if self.demo_mode:
            logger.info(f"[DEMO] get_client {client_id}")
            return {"id": client_id, "name": "Demo Client"}
        url = f"{self.base_url}/clients/{client_id}"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()
