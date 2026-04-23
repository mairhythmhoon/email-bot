# this is task is for daily one run only. 
# bday and festivals runs only one time.

import service
from datetime import datetime, timedelta
from Module import setup_logger
import json

def main():
    try:
        now = datetime.now().replace(microsecond=0)
        today = now.strftime("%d/%m")

        with open(service.BASE_DIR / "Data" / "data.json","r",encoding="utf-8") as f:
            data = json.load(f)

        if not service.festivals_list:
            service.error("\n>> No Festival Today.\n")
        else:
            service.info(f">>Today is {service.festivals_list}")
        
        brithday_sent = False

        for person in data:
            try:
                name = person["Name"]
                email = person["Email address"]

                try:       
                    if "Birthdate" in person:
                        person["Birthdate"] = datetime.strptime(person["Birthdate"], "%d/%m/%Y")
                except ValueError:
                    service.logger.exception("Date format is Corrupted")
                    service.error(">> Invalid date format")  

                # Check for brithdays
                if service.TEMPLATE_BDAY and person["Birthdate"].strftime("%d/%m") == today:
                    service.info(f">> Brithday Today: {name}")
                    if "{name}" not in service.TEMPLATE_BDAY:
                        service.logger.exception("Corrupted HTML file.")
                        raise ValueError("Missing placeholder in Join HTML template")
                    html1 = service.TEMPLATE_BDAY.replace("{name}",name)
                    if service.check_email(email):
                        if service.send_email_html(email,f"Happy Brithday {name}",html1,name):
                            birthday_sent = True
                            service.COUNTS["birthday"]+=1
                            service.COUNTS["total"]+=1
                    
                # Check for today's festival
                if (service.festivals_list)  and service.TEMPLATE_FESTIVAL:
                    festival = service.festivals_list[0]
                    if "{name}" not in service.TEMPLATE_FESTIVAL or "{festival}" not in service.TEMPLATE_FESTIVAL:
                        service.logger.exception("Corrupted HTML file.")
                        raise ValueError("Missing placeholder in Join HTML template")
                    html2 = service.TEMPLATE_FESTIVAL.replace("{name}",name).replace("{festival}",festival)
                    if service.check_email(email):
                        service.send_email_html(email,f"Warm Wishes on {festival}",html2,name)
                        service.COUNTS["festival"]+=1
                        service.COUNTS["total"]+=1
                    
            except Exception as e:
                service.logger.exception(f"Error for {person['Name']}: {e}")
                service.error(f"Error for {person['Name']}: {e}")    
        if not brithday_sent and (not service.festivals_list):
            service.logger.info(f">> No Birthdays today\t>> No festivals today")
            service.error(f">> No Birthdays today\n>> No festivals today")
    except Exception as e:
        service.logger.exception(f"Exception in main Execution : {e}")
        service.error(f"ERROR in main Execution : {e}")
        service.logger.info("===== EMAIL SYSTEM STOPED =====\n")
        exit(1)        
    finally:
        #   if same day have more then one festivals then next_run_date() is also same for it. 
        #   there for this will run at only last festivel of todays festival.
        if len(service.festivals_list)>1:
            service.logger.info("To Day is More then one Festival.")
            del service.festivals_list[0]
            service.logger.info("main() function runs another time")
            main()
            exit()  
        else:
            pass
        
if __name__ == "__main__":
    print ("")
    service.info ("███████╗███╗   ███╗ █████╗ ██╗██╗         ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗")
    service.info ("██╔════╝████╗ ████║██╔══██╗██║██║         ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝")
    service.info ("█████╗  ██╔████╔██║███████║██║██║         █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  ")
    service.info ("██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ")
    service.info ("███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗")
    service.info ("╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝")
    print("")
    #import time
    service.info("\n>> LEVEL 01 : Fetching Data From Database ")
    #time.sleep(3)
    try:
        service.get_data_from_google_sheet('Sheet-01')
        service.logger.info("Fetching Data From Database.")
    except Exception as e:
        service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
        service.error("\n>> Module Level Error in 'Google_Sheet.py'..." + e)
    service.info("\n>> LEVEL 01 IS DONE DATA IS GETING FROM DATABASE.\n")
    #time.sleep(3)
    
    service.info("\n>> LEVEL 02 : Running Algorithm For Festival and Brithday Mail Sending Task.")
    try:
        main()
    finally:
        if service.COUNTS["birthday"]==0 and service.COUNTS["failed"]==0 and service.COUNTS["festival"]==0 and  service.COUNTS["total"]==0:
            #time.sleep(3)
            service.logger.info("Nothing to add in Daily-Stats")
            service.info("\n>> Nothing to add in Daily-Stats")
        else:
            DAY_WISE_SUMMARY =[[datetime.now().strftime("%Y-%m-%d"),service.COUNTS["total"],service.COUNTS["birthday"],service.COUNTS["festival"],service.COUNTS["failed"]]]
            try:
                service.append_to_sheet("Task_01",DAY_WISE_SUMMARY)
                service.logger.info(DAY_WISE_SUMMARY)
            except Exception:
                service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
                service.error("\n>> Module Level Error in 'Google_Sheet.py'...")
        try:
            service.logger.info("Adding to Days Login data and Email Send Data.")
            service.log_login_attempt("System is Running Auto","******","******")
            service.append_to_sheet("Sheet-02", service.LOGIN_SHEET_DATA)
            service.append_to_sheet("Sheet-03", service.EMAIL_SHEET_DATA)
        except Exception as e:
            service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
            service.error("\n>> Module Level Error in 'Google_Sheet.py'..." + e)
        service.info ("███████╗███╗   ██╗██████╗      ██████╗ ███████╗    ██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗")
        service.info ("██╔════╝████╗  ██║██╔══██╗    ██╔═══██╗██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║")   
        service.info ("█████╗  ██╔██╗ ██║██║  ██║    ██║   ██║█████╗      ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║")
        service.info ("██╔══╝  ██║╚██╗██║██║  ██║    ██║   ██║██╔══╝      ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║")
        service.info ("███████╗██║ ╚████║██████╔╝    ╚██████╔╝██║         ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║")
        service.info ("╚══════╝╚═╝  ╚═══╝╚═════╝      ╚═════╝ ╚═╝         ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝")