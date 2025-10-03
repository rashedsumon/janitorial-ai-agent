# Janitorial AI Agent

## Setup
1. Copy `.env.example` to `.env` and fill the credentials.
2. (Optional) Put Kaggle dataset in `data/sample_hr.csv` or set `KAGGLE_SAMPLE_PATH` in `.env`.
3. Install requirements:
   pip install -r requirements.txt
4. Run Streamlit:
   streamlit run streamlit_app.py

## Notes
- Fill `JM_BASE_URL` and `JM_API_KEY` for Janitorial Manager real API.
- For Google Sheets set `GOOGLE_SERVICE_ACCOUNT_JSON` path to your service account JSON.
- For WhatsApp, either use Twilio or implement Meta's WhatsApp Cloud API.
- This app starts a background scheduler (APScheduler) on load — adjust cron in `scheduler_jobs`.
