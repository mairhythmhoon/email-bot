import json
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = f"Secure/credentials.json"
SPREADSHEET_ID = "1l_Nl_Q3sZnOlkCN4-rKRTUA865dJEN9kAU6xqOfWI7s"


def get_sheets_service():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build("sheets", "v4", credentials=credentials)


def get_data_from_google_sheet(range_):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()

        response = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_
        ).execute()

        values = response.get("values", [])

        if not values:
            logger.error("No data found in sheet.")
            return None

        headers = [h.strip() for h in values[0]]
        rows = values[1:]

        json_list = []

        for row in rows:
            obj = {}
            for i, key in enumerate(headers):
                obj[key] = row[i].strip() if i < len(row) else ""
            json_list.append(obj)

        output_path = f"Data/data.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_list, f, indent=4, ensure_ascii=False)

        logger.info("Data successfully written to data.json")
        return json_list

    except HttpError as e:
        logger.exception("Google Sheets API error occurred")
    except Exception:
        logger.exception("Unexpected error occurred")


def append_to_sheet(sheet_name, rows):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()

        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=sheet_name,
            valueInputOption="USER_ENTERED",
            body={"values": rows}
        ).execute()

        logger.info("Data appended successfully.")

    except HttpError:
        logger.exception("Google Sheets API append error")
    except Exception:
        logger.exception("Unexpected error while appending data")


# Dry run
if __name__ == "__main__":
    sheet_name = input("Enter sheet range : ")
    get_data_from_google_sheet(sheet_name)
