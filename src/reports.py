# src/reports.py
import os
import pandas as pd
from datetime import datetime
from jinja2 import Template
from .config import settings
from loguru import logger

ARTIFACT_DIR = os.path.join("artifacts", "reports")
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def generate_daily_report(df: pd.DataFrame, report_date: str = None):
    report_date = report_date or datetime.utcnow().strftime("%Y-%m-%d")
    fname_xlsx = os.path.join(ARTIFACT_DIR, f"daily_report_{report_date}.xlsx")
    df.to_excel(fname_xlsx, index=False)
    logger.info(f"XLSX report written: {fname_xlsx}")

    # Minimal HTML summary for PDF if desired
    summary = df.describe(include="all").to_html()
    template = Template("""
    <html><head><meta charset="utf-8"><title>Daily Report - {{date}}</title></head>
    <body>
    <h1>Daily Report - {{date}}</h1>
    <h2>Summary</h2>
    {{summary | safe}}
    </body></html>
    """)
    html = template.render(date=report_date, summary=summary)
    fname_html = os.path.join(ARTIFACT_DIR, f"daily_report_{report_date}.html")
    with open(fname_html, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"HTML report written: {fname_html}")

    # Optional PDF export (requires wkhtmltopdf)
    try:
        import pdfkit
        fname_pdf = os.path.join(ARTIFACT_DIR, f"daily_report_{report_date}.pdf")
        pdfkit.from_file(fname_html, fname_pdf)
        logger.info(f"PDF report written: {fname_pdf}")
    except Exception as e:
        logger.warning(f"PDF generation skipped or failed: {e}")

    return {"xlsx": fname_xlsx, "html": fname_html}
