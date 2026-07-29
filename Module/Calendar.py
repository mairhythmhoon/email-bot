# Developed By github.com/@mairhythmhoon

import requests
import json
from datetime import datetime


def main_():
    import logging

    logger = logging.getLogger(__name__)

    CURRENT_YEAR = datetime.now().year

    CALENDARS = {
        "Hindu": "https://calendar.google.com/calendar/ical/en.hinduism%23holiday%40group.v.calendar.google.com/public/basic.ics",
        "Indian": "https://calendar.google.com/calendar/ical/en-in.indian%23holiday%40group.v.calendar.google.com/public/basic.ics",
    }

    OUTPUT_FILE = "Data/festivals.json"

    if not OUTPUT_FILE:
        logger.exception("festivals.json path is not found.")
        return

    def parse_ics(ics_text, calendar_name):
        events = []
        lines = ics_text.splitlines()
        event = {}

        for line in lines:
            line = line.strip()

            if line == "BEGIN:VEVENT":
                event = {}

            elif line.startswith("DTSTART"):
                date_raw = line.split(":")[-1][:8]
                event_date = datetime.strptime(date_raw, "%Y%m%d")

                # Save date in DD-MM-YYYY format
                event["date"] = event_date.strftime("%d-%m-%Y")

            elif line.startswith("SUMMARY"):
                event["festival_name"] = line.split(":", 1)[1]

            elif line == "END:VEVENT":
                if (
                    "date" in event
                    and "festival_name" in event
                    and datetime.strptime(
                        event["date"], "%d-%m-%Y"
                    ).year == CURRENT_YEAR
                ):
                    event["calendar"] = calendar_name
                    events.append(event)

        return events

    all_events = []

    for calendar_name, url in CALENDARS.items():
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            all_events.extend(parse_ics(response.text, calendar_name))

        except requests.RequestException as e:
            logger.exception(f"Failed to fetch {calendar_name} calendar: {e}")

    # Merge duplicate festivals
    merged_events = {}

    for event in all_events:
        key = (event["date"], event["festival_name"])

        if key not in merged_events:
            merged_events[key] = event
        else:
            # Same festival exists in another calendar
            merged_events[key]["calendar"] = "merged"

    # Sort by date
    final_events = sorted(
        merged_events.values(),
        key=lambda x: datetime.strptime(x["date"], "%d-%m-%Y"),
    )

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(final_events, file, indent=4, ensure_ascii=False)

    except FileNotFoundError as e:
        logger.exception(f"Output file not found: {e}")


if __name__ == "__main__":
    main_()