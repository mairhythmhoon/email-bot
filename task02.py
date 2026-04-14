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
        
        joining_sent = False

        for person in data:
            try:
                name = person["Name"]
                email = person["Email address"]

                try:       
                    if "Timestamp" in person:
                        person["Timestamp"] = datetime.strptime(person["Timestamp"], "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    service.logger.exception("Date format is Corrupted")
                    service.error(">> Invalid date format")  

                # Joining Emaile (Last 24 hrs)
                join_time = person["Timestamp"]
                if service.TEMPLATE_JOIN and timedelta(0) <= (now - join_time) <= timedelta(hours=24):
                    service.info(f">> New Joiner: {name}")
                    join_str = join_time.strftime("%d/%m/%Y %H:%M:%S")
                    if "{name}" not in service.TEMPLATE_JOIN or "{join_time_str}" not in service.TEMPLATE_JOIN:
                        service.logger.exception("Corrupted HTML file.")
                        raise ValueError("Missing placeholder in Join HTML template")
                    html0 = service.TEMPLATE_JOIN.replace("{name}",name).replace("{join_time_str}",join_str)
                    if service.check_email(email):
                        if service.send_email_html(email,f"Thank You for Joining Us, {name}",html0,name):
                            joining_sent = True
                            service.COUNTS["joining"]+=1
                            service.COUNTS["total"]+=1
                    
            except Exception as e:
                service.logger.exception(f"Error for {person["Name"]}: {e}")
                service.error(f"Error for {person["Name"]}: {e}")    
        
        if not joining_sent:
            service.logger.info(f">> No new joiners in last 24 hrs")
            service.error(f">> No new joiners in last 24 hrs\n")
    
    except Exception as e:
        service.logger.exception(f"Exception in main Execution : {e}")
        service.error(f"ERROR in main Execution : {e}")
        service.logger.info("===== EMAIL SYSTEM STOPED =====\n")
        exit(1)        
    
if __name__ == "__main__":
    print ("")
    service.info ("███████╗███╗   ███╗ █████╗ ██╗██╗         ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗")
    service.info ("██╔════╝████╗ ████║██╔══██╗██║██║         ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝")
    service.info ("█████╗  ██╔████╔██║███████║██║██║         █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  ")
    service.info ("██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ")
    service.info ("███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗")
    service.info ("╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝")
    print("")
    import time
    service.info("\n>> LEVEL 01 : Fetching Data From Database ")
    time.sleep(3)
    try:
        service.get_data_from_google_sheet('Sheet-01')
        service.logger.info("Fetching Data From Database.")
    except Exception as e:
        service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
        service.error("\n>> Module Level Error in 'Google_Sheet.py'..." + e)
    service.info("\n>> LEVEL 01 IS DONE DATA IS GETING FROM DATABASE.\n")
    time.sleep(3)
    
    service.info("\n>> LEVEL 02 : Running Algorithm For Main Task.")
    try:
        main()
    finally:
        if service.COUNTS["failed"]==0 and service.COUNTS["joining"]==0 and service.COUNTS["total"]==0:
            time.sleep(3)
            service.logger.info("Nothing to add in Daily-Stats")
            service.info("\n>> Nothing to add in Daily-Stats")
        else:
            DAY_WISE_SUMMARY =[[datetime.now().strftime("%Y-%m-%d"),service.COUNTS["total"],service.COUNTS["joining"],service.COUNTS["failed"]]]
            try:
                service.append_to_sheet("Task_02",DAY_WISE_SUMMARY)
                service.logger.info(DAY_WISE_SUMMARY)
            except Exception:
                service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
                service.error("\n>> Module Level Error in 'Google_Sheet.py'...")
        try:
            service.logger.info("Adding to Days Login data and Email Send Data.")
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