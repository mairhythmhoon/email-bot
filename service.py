import os 
import re
import json
import smtplib
import dns.resolver
import random
import sys
from sys import exit
from dotenv import load_dotenv
from colorama import Fore,Style,init
from datetime import datetime, timedelta
from pathlib import Path
from email.message import EmailMessage
from Module import get_data_from_google_sheet,append_to_sheet 
from Module import main_
from Module import birthday_filter,festival_filter
from Module import setup_logger

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

COUNTS = {
    "total":0,
    "birthday":0,
    "festival":0,
    "failed":0,
    "joining":0

}

logger = setup_logger()
logger.info("===== EMAIL SYSTEM STARTED =====")

# for color font
init(autoreset=True)
def info(msg):
    print(Fore.YELLOW + msg)
def error(msg):
    print(Fore.RED + msg)

try:
    load_dotenv(BASE_DIR / "Secure" / ".env")
    logger.info(".env file is loaded")
except Exception:
    logger.exception(".env file is not found/Exception in loading")
    error("\n>> .env File Is Not Present")
    exit()
try:
    main_() 
    logger.info("Calendar.py Module's main_() is Running")
except Exception as e:
    error("\n>> Module Level Error in 'Calendar.py'...")
    logger.exception("Exception in Calender.py")
    error(e)

EMAIL = os.getenv("E_MAIL")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 465

# Firewall For E-mail Address Checking
def check_email(email):
    email = email.strip()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'   #This regex is simple it checks the general format but not all edge cases like multiple dots or invalid domains.
    if not re.match(pattern, email):
        error(f"\nInvalid email format: {email}")
        return False
    domain = email.split('@')[-1].strip()
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return True
    except dns.resolver.NXDOMAIN:
        error(f"\nInvalid domain for {email}: Domain does not exist.")
        logger.exception(f"Invalid domain for {email}: Domain does not exist.")
    except dns.resolver.NoAnswer:
        error(f"\nNo MX record found for {email}.")
        logger.exception(f"No MX record found for {email}.")
    except dns.resolver.NoNameservers:
        error(f"\nNo name servers for domain of {email}.")
        logger.exception(f"No name servers for domain of {email}.")
    except Exception as e:
        error(f"\nUnknown error for {email}: {e}")
        logger.exception(f"Unknown error for {email}: {e}")
    return False

def send_email_html(to, subject, html_content,name):
    try:
        msg = EmailMessage()
        msg['From'] = f"Ridham Parmar <{EMAIL}>" 
        msg['To'] = f"{name} <{to}>"
        msg['Subject'] = subject
        msg['Reply-To'] = os.getenv("RESPONS_MAILE")   
        msg.set_content("This is an HTML email.")
        msg.add_alternative(html_content, subtype='html')
     
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.login(EMAIL, PASSWORD)
       
        smtp.send_message(msg)
        records_of_email_sended(EMAIL,to,subject)
        print(Fore.GREEN+f"\n>> Email sent to {to} | Subject: {subject}\n")
        return True
    except Exception as e:
        error(f"ERROR while sending email to {to} : {e}")
        logger.exception(f"ERROR while sending email to {to} : {e}")
        COUNTS["failed"] +=1
        return False

# Load HTML templates ass Strings
def load_template(filename):
    try:
        path = os.path.join(os.path.dirname(__file__),"Template", filename)
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logger.exception(f"Error loading HTML template {filename}: {e}")
        error(f"Error loading HTML template {filename}: {e}")
        return None

try:  
    TEMPLATE_JOIN = load_template("Thank_You_Mail.html")
    TEMPLATE_BDAY = load_template("Birthday_Wishing_Mail.html")
    TEMPLATE_FESTIVAL = load_template("Festival_Mail.html")
    TWO_FACTOR_AUTHENTICATION_PROCESS = load_template("Two_Factor_Authentication.html")
    INTERNAL_MESSAGE = load_template("Future_TaskPlanning.html")
except Exception:
    logger.exception("Templates Is Not Present.")
    error("\n>> Template Is Not Present.")

#this function get festival is today
def load_festivals_for_today(json_path):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(json_path, "r", encoding="utf-8") as f:
        festivals = json.load(f)
    for person in festivals:
        try:
            if "date" in festivals:
                festivals["date"] = datetime.strptime(festivals["date"],"%d/%m/%Y")
        except ValueError:
            error("Error")

        today_festivals = [
            f["festival_name"]
            for f in festivals
            if f["date"] == today
        ]
    return today_festivals

# this is normally list 
try:
    logger.info("Todays Festivals is loaded in program.")
    festivals_list = load_festivals_for_today(BASE_DIR / "Data" / "festivals.json")
except Exception:
    logger.exception("festival.json is not found")
    error("\n>> 'festival.json' File Is Not Present.")

   
# Row Data Set for inserting Data into Google Sheet
EMAIL_SHEET_DATA = []
LOGIN_SHEET_DATA = []

# Email sended Record
def records_of_email_sended(From, To, Subject):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Locally inserting Data
    EMAIL_SHEET_DATA.append([
        now,
        From,
        To,
        Subject
    ])

def log_login_attempt(status="System is Running Auto", entered_otp="******", correct_otp="******"):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    # Locally inseting Data into Google Sheet
    LOGIN_SHEET_DATA.append([now,"System is Running Auto",entered_otp,correct_otp,"# This is Running From GitHub."])