import service
from datetime import datetime, timedelta
from Module import setup_logger
import json
import time

# File to store last processed timestamp
LAST_RUN_FILE = service.BASE_DIR / "Data" / "last_run.json"


def load_last_run():
    try:
        if not LAST_RUN_FILE.exists():
            return None

        with open(LAST_RUN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("last_timestamp"):
            return None

        return datetime.strptime(data["last_timestamp"], "%d/%m/%Y %H:%M:%S")

    except Exception:
        return None

def save_last_run(timestamp):
    with open(LAST_RUN_FILE, "w",encoding="utf-8") as f:
        json.dump({
            "last_timestamp": timestamp.strftime("%d/%m/%Y %H:%M:%S")
        }, f)

def main():
    try:
        run_time = datetime.now().replace(microsecond=0)

        with open(service.BASE_DIR / "Data" / "data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        last_run_time = load_last_run()

        # If file missing or empty
        if last_run_time is None:
            start_time = run_time - timedelta(hours=24)
            save_last_run(run_time)   # first time save current runtime
        else:
            start_time = last_run_time

        joining_sent = False

        for person in data:
            try:
                name = person["Name"]
                email = person["Email address"]

                if "Timestamp" not in person:
                    continue

                try:
                    join_time = datetime.strptime(
                        person["Timestamp"],
                        "%d/%m/%Y %H:%M:%S"
                    )
                except ValueError:
                    service.logger.exception("Date format corrupted")
                    continue

                # Filter records between start_time and current run_time
                if start_time <= join_time <= run_time:

                    service.info(f">> New Joiner: {name}")

                    join_str = join_time.strftime("%d/%m/%Y %H:%M:%S")

                    if "{name}" not in service.TEMPLATE_JOIN or "{join_time_str}" not in service.TEMPLATE_JOIN:
                        raise ValueError("Missing placeholder in Join HTML template")

                    html0 = (
                        service.TEMPLATE_JOIN
                        .replace("{name}", name)
                        .replace("{join_time_str}", join_str)
                    )

                    if service.check_email(email):
                        if service.send_email_html(
                            email,
                            f"Thank You for Joining Us, {name}",
                            html0,
                            name
                        ):
                            joining_sent = True
                            service.COUNTS["joining"] += 1
                            service.COUNTS["total"] += 1

            except Exception as e:
                service.logger.exception(f"Error for {person.get('Name', 'Unknown')}: {e}")

        # Save current runtime after all processing
        save_last_run(run_time)

        if not joining_sent:
            service.logger.info(">> No new joiners since last run")
            service.info(">> No new joiners since last run")

    except Exception as e:
        service.logger.exception(f"Exception in main execution: {e}")
        service.error(f"ERROR in main execution: {e}")

if __name__ == "__main__":

    print("")
    service.info("███████╗███╗   ███╗ █████╗ ██╗██╗         ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗")
    service.info("██╔════╝████╗ ████║██╔══██╗██║██║         ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝")
    service.info("█████╗  ██╔████╔██║███████║██║██║         █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  ")
    service.info("██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ")
    service.info("███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗")
    service.info("╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝")
    print("")

    service.info("\n>> LEVEL 01 : Fetching Data From Database ")
    time.sleep(3)

    try:
        service.get_data_from_google_sheet('Sheet-01')
        service.logger.info("Fetching Data From Database.")
    except Exception as e:
        service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
        service.error("\n>> Module Level Error in 'Google_Sheet.py'..." + str(e))

    service.info("\n>> LEVEL 01 IS DONE DATA IS GETTING FROM DATABASE.\n")
    time.sleep(3)

    service.info("\n>> LEVEL 02 : Running Algorithm For New Joiners Sending Mails Task.")
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y %H:%M:%S")

    service.info(f"\n>> From {load_last_run()} to {formatted_time}.")

    try:
        main()
    finally:
        if service.COUNTS["failed"] == 0 and service.COUNTS["joining"] == 0 and service.COUNTS["total"] == 0:
            time.sleep(3)
            service.logger.info("Nothing to add in Daily-Stats")
            service.info("\n>> Nothing to add in Daily-Stats")
        else:
            DAY_WISE_SUMMARY = [[
                datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                service.COUNTS["total"],
                service.COUNTS["joining"],
                service.COUNTS["failed"]
            ]]
            try:
                service.append_to_sheet("Task_02", DAY_WISE_SUMMARY)
                service.logger.info(DAY_WISE_SUMMARY)
            except Exception:
                service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
                service.error("\n>> Module Level Error in 'Google_Sheet.py'...")

        try:
            service.logger.info("Adding to Days Login data and Email Send Data.")
            service.log_login_attempt("System is Running Auto","######","######")
            service.append_to_sheet("Sheet-02", service.LOGIN_SHEET_DATA)
            service.append_to_sheet("Sheet-03", service.EMAIL_SHEET_DATA)
        except Exception as e:
            service.logger.exception("Module Level Error in 'Google_Sheet.py'.")
            service.error("\n>> Module Level Error in 'Google_Sheet.py'..." + str(e))

        service.info("███████╗███╗   ██╗██████╗      ██████╗ ███████╗    ██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗")
        service.info("██╔════╝████╗  ██║██╔══██╗    ██╔═══██╗██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║")   
        service.info("█████╗  ██╔██╗ ██║██║  ██║    ██║   ██║█████╗      ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║")
        service.info("██╔══╝  ██║╚██╗██║██║  ██║    ██║   ██║██╔══╝      ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║")
        service.info("███████╗██║ ╚████║██████╔╝    ╚██████╔╝██║         ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║")
        service.info("╚══════╝╚═╝  ╚═══╝╚═════╝      ╚═════╝ ╚═╝         ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝")