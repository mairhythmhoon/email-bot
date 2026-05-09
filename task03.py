# Developed By github.com/@mairhythmhoon 
import os
import smtplib
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from service import TEMPLATE_LOG         # Internal Module variable from service.py
from colorama import Fore,Style,init
from email.message import EmailMessage

BASE_DIR = Path(__file__).resolve().parent

LOG_FOLDER = "Logs"  

try:
    load_dotenv(BASE_DIR / "Secure" / ".env")
except Exception:
    print("\n>> .env File Is Not Present")
    exit()

SENDER_EMAIL = os.getenv("E_MAIL")
SENDER_PASSWORD = os.getenv("PASSWORD")
RECEIVER_EMAIL = os.getenv("RESPONS_MAILE")
MONTH = datetime.now().strftime("%B")

# Create temp zip path
ZIP_FILE = os.path.join(tempfile.gettempdir(), f"Log_Report-{MONTH}.zip")

def zip_logs():
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(LOG_FOLDER):
            for file in files:
                if file.endswith(".log"):
                    filepath = os.path.join(root, file)

                    # preserve folder structure inside zip
                    arcname = os.path.relpath(filepath, LOG_FOLDER)

                    zipf.write(filepath, arcname)

    print(f"Logs zipped at: {ZIP_FILE}")

# sending maile with .zip file 
def send_email(html,month):
    try:
        msg = EmailMessage()
        msg['From'] = f"System <{SENDER_EMAIL}>"
        msg['To'] = f"Admin <{RECEIVER_EMAIL}>"
        msg['Subject'] = f"Monthly Log Files Report From System - {month}"
        msg['Reply-To'] = os.getenv("E_MAIL")
        msg.set_content("This is an HTML email.")
        msg.add_alternative(html, subtype='html')
    
        with open(ZIP_FILE, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='zip',
                filename=f"Log_Report-{month}.zip"
            )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e :
        print(f"ERROR while sending email.")
        return False

# cleanup .zip file from tem store.
def cleanup():
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)
        print("Temporary zip file deleted.")

if __name__ == "__main__": 
    month = datetime.now().strftime("%B")
    try:
        zip_logs()
        if TEMPLATE_LOG:
            if "{month}" not in TEMPLATE_LOG:
                raise ValueError("Missing placeholdet in log HTML template")
            html2 = TEMPLATE_LOG.replace("{month}",month)
            send_email(html2,month)
    finally:
        cleanup()