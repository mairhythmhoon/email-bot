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

def log_login_attempt(status, entered_otp="******", correct_otp="******"):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    # Locally inseting Data into Google Sheet
    LOGIN_SHEET_DATA.append([now,"System is Running Auto",entered_otp,correct_otp])

# def two_factor_authentication_process():
#     info("\nLogin Required\n1. Yes\n2. No")
#     choice = input(Fore.YELLOW+"\n>> Enter choice: ").strip()

#     if choice != "1":
#         logger.exception("User cncelled login and Exiting program.")
#         info(">> Exiting program...")
#         log_login_attempt("CANCELLED")
#         try:
#             append_to_sheet("Sheet-02", LOGIN_SHEET_DATA)
#             append_to_sheet("Sheet-03", EMAIL_SHEET_DATA)
#         except Exception:
#             logger.exception("\nModule Level Error in 'Google_Sheet.py'.")
#             error("\n>> Module Level Error in 'Google_Sheet.py'...")
#         logger.info("===== EMAIL SYSTEM STOPED =====\n")
#         exit(0)

#     # Generate OTP
#     otp = random.randint(100000, 999999)
#     html_template = TWO_FACTOR_AUTHENTICATION_PROCESS
#     if "{******}" not in TWO_FACTOR_AUTHENTICATION_PROCESS:
#         logger.exception("Corrupted HTML file.")
#         raise ValueError("Missing placeholder in Join HTML template")
#     html_content = html_template.replace("{******}", str(otp))

#     # Send OTP to your own email
#     if send_email_html(os.getenv("RESPONS_MAILE") , "Two Factor Authentication Process", html_content,name="OTP Verification Code"):
#         print(Fore.GREEN+">> OTP sent to your email.")
        
#         logger.info("OTP sent to your email.")
#         entered_otp = input(Fore.YELLOW+"\n>> Enter the 6-Digit OTP received in your email: ").strip()
#         logger.info(f"Entered OTP is : {entered_otp}.")

#         if entered_otp == str(otp):
#             print(Fore.GREEN+"\n>> OTP Verified Successfully!\n")
#             #log_login_attempt("SUCCESS", entered_otp, otp) -> This makes bug in Google Sheets entrys
#             info("Are you logging in?\n1. Yes, I am in\n2. No, I am not in")
#             final_choice = input(Fore.YELLOW+">> Enter choice: ").strip()
#             if final_choice == "1":
#                 log_login_attempt("SUCCESS", entered_otp, otp)
#                 return True
#             else:
#                 logger.exception("User is Exiting After Verify.")
#                 info(">> Exiting program...")               
#                 log_login_attempt("CANCELLED_AFTER_VERIFY", entered_otp,otp)
#                 try:
#                     append_to_sheet("Sheet-03", EMAIL_SHEET_DATA)
#                     append_to_sheet("Sheet-02", LOGIN_SHEET_DATA)
#                 except Exception:
#                     logger.exception("Module Level Error in 'Google_Sheet.py'...")
#                     error("\n>> Module Level Error in 'Google_Sheet.py'...")
#                 logger.info("===== EMAIL SYSTEM STOPED =====\n")
#                 exit(0)
#         else:
#             logger.info("Invalid OTP!.")
#             error("Invalid OTP!")
#             info(">> Exiting program...")
#             log_login_attempt("FAIL", entered_otp,otp)
#             try:
#                 append_to_sheet("Sheet-03", EMAIL_SHEET_DATA)
#                 append_to_sheet("Sheet-02", LOGIN_SHEET_DATA)
#             except Exception:
#                 logger.exception("Module Level Error in 'Google_Sheet.py'.")
#                 error("\n>> Module Level Error in 'Google_Sheet.py'...")
#             logger.info("===== EMAIL SYSTEM STOPED =====\n")
#             exit(0)
#     else:
#         logger.info("OTP Sending is Failed.")
#         error(">> Failed to send OTP. Exiting...")
#         log_login_attempt("OTP_SEND_FAIL")
#         try:   
#             append_to_sheet("Sheet-03", EMAIL_SHEET_DATA)
#             append_to_sheet("Sheet-02", LOGIN_SHEET_DATA)
#         except Exception:
#             logger.exception("Module Level Error in 'Google_Sheet.py'.")
#             error("\n>> Module Level Error in 'Google_Sheet.py'...")
#         logger.info("===== EMAIL SYSTEM STOPED =====\n")
#         exit(0) 

# def next_run_date():
#     try:
#         with open(BASE_DIR / "Data" / "data.json", "r", encoding="utf-8") as f:
#             bday_data = json.load(f)

#         with open(BASE_DIR / "Data" / "festivals.json", "r", encoding="utf-8") as f:
#             fest_data = json.load(f)

#         a = birthday_filter(bday_data)
#         b = festival_filter(fest_data)
        
#         bday_content = ""
#         for item in a:
#             bday_content += f" • <span class='highlight'>  Name</span> : {item['name']}<br><span class='highlight'>&emsp;Emaile </span>: {item['email']} <br> <span class='highlight'>&emsp;Date</span>:<strong>{item['date']}</strong><br><br>"
        
#         fest_content = ""
#         for item in b:
#             fest_content += f" • <span class='highlight'>{item['name']}</span> - <strong>{item['date']}</strong><br>"
        
#         #MAILE SEDING 
#         if ("{bdaytask}" not in INTERNAL_MESSAGE) and ("{festtask}" not in INTERNAL_MESSAGE):
#             logger.exception("Corrupted HTML file.")
#             raise ValueError("Missing placeholder in Join HTML template")
#         htmltemplet = INTERNAL_MESSAGE.replace("{bdaytask}",bday_content).replace("{festtask}",fest_content)
#         send_email_html(os.getenv("RESPONS_MAILE") , "INTERNAL MESSAGE FROM SYSTEM", htmltemplet,name="INTERNAL MESSAGE")
        
#     except Exception as e:
#         logger.exception("Module Level Error in 'Admin_Sysytem_Module.py'.")
#         error("\n>> Module Level Error in 'Admin_Sysytem_Module.py'...")
#         error(e)

# Main Functions    
def main():
    logger.info("Running main Logic of this program.")
    try:
        now = datetime.now().replace(microsecond=0)
        today = now.strftime("%d/%m")
        
        with open(BASE_DIR / "Data" / "data.json","r",encoding="utf-8") as f:
            data = json.load(f)

        if not festivals_list:
           error("\n>> No festival today.\n")
        else:
            info(f"\n>> Today is {festivals_list}")
            
        birthday_sent = False
        joining_sent = False

        for person in data:
            try:
                name = person["Name"]
                email = person["Email address"]
        
                # DATA STRING TO DATE FORMET Convert
                try:       
                    if "Birthdate" in person:
                        person["Birthdate"] = datetime.strptime(person["Birthdate"], "%d/%m/%Y")
                    if "Timestamp" in person:
                        person["Timestamp"] = datetime.strptime(person["Timestamp"], "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    logger.exception("Date format is Corrupted")
                    error(">> Invalid date format")

                # Joining Emaile (Last 24 hrs)
                join_time = person["Timestamp"]
                if TEMPLATE_JOIN and timedelta(0) <= (now - join_time) <= timedelta(hours=24):
                    info(f">> New Joiner: {name}")
                    join_str = join_time.strftime("%d/%m/%Y %H:%M:%S")
                    if "{name}" not in TEMPLATE_JOIN or "{join_time_str}" not in TEMPLATE_JOIN:
                        logger.exception("Corrupted HTML file.")
                        raise ValueError("Missing placeholder in Join HTML template")
                    html0 = TEMPLATE_JOIN.replace("{name}",name).replace("{join_time_str}",join_str)
                    if check_email(email):
                        if send_email_html(email,f"Thank You for Joining Us, {name}",html0,name):
                            joining_sent = True
                            COUNTS["joining"]+=1
                            COUNTS["total"]+=1
                            
                # Check for brithdays
                if TEMPLATE_BDAY and person["Birthdate"].strftime("%d/%m") == today:
                    info(f">> Brithday Today: {name}")
                    if "{name}" not in TEMPLATE_BDAY:
                        logger.exception("Corrupted HTML file.")
                        raise ValueError("Missing placeholder in Join HTML template")
                    html1 = TEMPLATE_BDAY.replace("{name}",name)
                    if check_email(email):
                        if send_email_html(email,f"Happy Brithday {name}",html1,name):
                            birthday_sent = True
                            COUNTS["birthday"]+=1
                            COUNTS["total"]+=1
                
                # Check for today's festival
                if (festivals_list)  and TEMPLATE_FESTIVAL:
                    festival = festivals_list[0]
                    if "{name}" not in TEMPLATE_FESTIVAL or "{festival}" not in TEMPLATE_FESTIVAL:
                        logger.exception("Corrupted HTML file.")
                        raise ValueError("Missing placeholder in Join HTML template")
                    html2 = TEMPLATE_FESTIVAL.replace("{name}",name).replace("{festival}",festival)
                    if check_email(email):
                        send_email_html(email,f"Warm Wishes on {festival}",html2,name)
                        COUNTS["festival"]+=1
                        COUNTS["total"]+=1
                
            except Exception as e:
                logger.exception(f"Error for {person['Name']}: {e}")
                error(f"Error for {person['Name']}: {e}")    
                
        if not birthday_sent and (not festivals_list) and not joining_sent:
            import time 
            logger.info(f">> No Birthdays today\t>> No festivals today\t>> No new joiners in last 24 hrs")
            error(f">> No Birthdays today\n>> No festivals today\n>> No new joiners in last 24 hrs\n")
    except Exception as e:
        logger.exception(f"Exception in main Execution : {e}")
        error(f"ERROR in main Execution : {e}")
        logger.info("===== EMAIL SYSTEM STOPED =====\n")
        exit(1)
    finally:
        #   if same day have more then one festivals then next_run_date() is also same for it. 
        #   there for this will run at only last festivel of todays festival.
        if len(festivals_list)>1:
            logger.info("To Day is More then one Festival.")
            del festivals_list[0]
            logger.info("main() function runs another time")
            main()
            exit()  #------this solves the problem of tow time run after this code.------#
                    #----code that runs many time as per festival-----#
                    
                    # else:
                    #     passw
                    # try:
                    #     next_run_date()
                    # except Exception as e:
                    #     error("\n>> Module Level Error in 'Admin_System_Module.py'...")
        else:
            pass