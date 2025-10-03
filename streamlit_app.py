# streamlit_app.py
import streamlit as st
import os
from src.config import settings
from src.utils import load_sample_data
from src.jm_client import JanitorialManagerClient
from src.google_sheets import GoogleSheetsClient
from src.whatsapp import WhatsAppClient
from src.reports import generate_daily_report
from src.scheduler_jobs import start_scheduler
from loguru import logger

st.set_page_config(page_title="Janitorial AI Agent", layout="wide")

st.title("Janitorial Manager — AI Agent Control Panel")
st.markdown("Manage automation, view logs, run jobs, and test integrations.")

# Start scheduler on app load (background)
if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state["scheduler_started"] = True
    st.info("Background scheduler started (daily jobs).")

col1, col2 = st.columns(2)

with col1:
    st.header("Demo / Data")
    st.write("DEMO_MODE:", settings.DEMO_MODE)
    st.write("Sample data path:", settings.KAGGLE_SAMPLE_PATH)
    if st.button("Load sample Kaggle dataset"):
        df = load_sample_data()
        if df.empty:
            st.warning("Failed to load sample dataset. Check path and .env settings.")
        else:
            st.session_state["sample_df"] = df
            st.success(f"Loaded sample dataset ({len(df)} rows).")
            st.dataframe(df.head(50))

    if "sample_df" in st.session_state:
        df = st.session_state["sample_df"]
        st.download_button("Download sample as CSV", df.to_csv(index=False), file_name="sample_hr.csv", mime="text/csv")

with col2:
    st.header("Actions")
    jm = JanitorialManagerClient()
    ga = GoogleSheetsClient()
    wa = WhatsAppClient()

    st.subheader("Create Demo Client")
    client_name = st.text_input("Client name", "Demo Client A")
    client_address = st.text_input("Address", "123 Demo St")
    if st.button("Create client in Janitorial Manager"):
        res = jm.create_client({"name": client_name, "address": client_address})
        st.json(res)

    st.subheader("Send WhatsApp message (test)")
    to_number = st.text_input("To (E.164)", "+8801XXXXXXXXX")
    message = st.text_area("Message", "Reminder: your shift starts at 6 PM")
    if st.button("Send WA"):
        res = wa.send_message(to_whatsapp_number=to_number, body=message)
        st.json(res)

st.markdown("---")
st.header("Reports")
if st.button("Generate daily report (now)"):
    if "sample_df" not in st.session_state:
        st.warning("Load the sample dataset first or connect live data.")
    else:
        files = generate_daily_report(st.session_state["sample_df"].head(200))
        st.success("Report generated.")
        st.write(files)
        with open(files["xlsx"], "rb") as f:
            st.download_button("Download XLSX", f, file_name=os.path.basename(files["xlsx"]), mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
