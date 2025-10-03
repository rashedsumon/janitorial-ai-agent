# src/google_sheets.py
import os
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
from .config import settings
from loguru import logger

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

class GoogleSheetsClient:
    def __init__(self, service_account_json=None):
        self.service_account_json = service_account_json or settings.GOOGLE_SERVICE_ACCOUNT_JSON
        if self.service_account_json and os.path.exists(self.service_account_json):
            creds = Credentials.from_service_account_file(self.service_account_json, scopes=SCOPES)
            self.gc = gspread.authorize(creds)
            logger.info("Google Sheets client initialized.")
        else:
            self.gc = None
            logger.warning("Google service account key missing or not found; Sheets client not initialized.")

    def read_sheet_as_df(self, spreadsheet_key_or_url, sheet_name=0):
        if not self.gc:
            logger.error("Google Sheets client not available.")
            return pd.DataFrame()
        sh = self.gc.open_by_key(spreadsheet_key_or_url) if len(spreadsheet_key_or_url) == 44 else self.gc.open_by_url(spreadsheet_key_or_url)
        worksheet = sh.get_worksheet(sheet_name) if isinstance(sheet_name, int) else sh.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)

    def write_df_to_sheet(self, spreadsheet_key_or_url, df: pd.DataFrame, sheet_name="Sheet1"):
        if not self.gc:
            raise RuntimeError("Google Sheets client not available.")
        sh = self.gc.open_by_key(spreadsheet_key_or_url) if len(spreadsheet_key_or_url) == 44 else self.gc.open_by_url(spreadsheet_key_or_url)
        try:
            worksheet = sh.worksheet(sheet_name)
            sh.del_worksheet(worksheet)
        except Exception:
            pass
        worksheet = sh.add_worksheet(title=sheet_name, rows=str(len(df)+10), cols=str(len(df.columns)+5))
        worksheet.update([df.columns.values.tolist()] + df.fillna("").values.tolist())
        logger.info("Dataframe written to sheet.")
