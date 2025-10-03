# src/scheduler_jobs.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from .config import settings
from .utils import load_sample_data
from .reports import generate_daily_report
from .jm_client import JanitorialManagerClient
from .whatsapp import WhatsAppClient
from loguru import logger
import pandas as pd

scheduler = BackgroundScheduler(timezone=settings.SCHEDULER_TIMEZONE)

def daily_report_job():
    logger.info("Running daily_report_job")
    # For demo - load sample data and compute simple metrics for report
    df = load_sample_data()
    if df.empty:
        logger.warning("No data for report.")
        return
    # Example: summarize hours by employee — using dataset as stand-in
    # In real usage, pull crew/time entries from JanitorialManager API or Google Sheets
    report_df = pd.DataFrame({
        "Employee": df.get("EmployeeNumber", range(len(df))).astype(str),
        "Attrition": df.get("Attrition", ""),
        "MonthlyIncome": df.get("MonthlyIncome", 0)
    }).head(50)
    files = generate_daily_report(report_df)
    logger.info(f"Daily report created: {files}")

    # Example sending a WhatsApp notification to manager
    wa = WhatsAppClient()
    wa.send_message(to_whatsapp_number="+8801XXXXXXXXX", body=f"Daily report generated: {files.get('xlsx')}")

def start_scheduler():
    # schedule daily at 18:00 using CronTrigger or use provided cron in env
    scheduler.add_job(daily_report_job, CronTrigger(hour=18, minute=0, timezone=settings.SCHEDULER_TIMEZONE))
    scheduler.start()
    logger.info("Scheduler started with daily report job.")
