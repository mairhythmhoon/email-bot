import requests
import json
from datetime import datetime

def main_():
    import logging

    logger = logging.getLogger(__name__)
    
    CURRENT_YEAR = datetime.now().year

    CALENDARS = {
        "Hindu": f"https://calendar.google.com/calendar/ical/en.hinduism%23holiday%40group.v.calendar.google.com/public/basic.ics",
        "Indian": f"https://calendar.google.com/calendar/ical/en-in.indian%23holiday%40group.v.calendar.google.com/public/basic.ics"
    }

    OUTPUT_FILE = f"Data/festivals.json"
    if not OUTPUT_FILE:
        logger.exception("festival.json is not found.")
        exit(0)
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
                event["date"] = event_date.strftime("%Y-%m-%d")
            elif line.startswith("SUMMARY"):
                event["festival_name"] = line.split(":", 1)[1]
            elif line == "END:VEVENT":
                if (
                    "date" in event
                    and "festival_name" in event
                    and datetime.strptime(event["date"], "%Y-%m-%d").year == CURRENT_YEAR
                ):
                    event["calendar"] = calendar_name
                    events.append(event)
        return events
    
    all_events = []
    for calendar_name, url in CALENDARS.items():
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        all_events.extend(parse_ics(response.text, calendar_name))
    # merge same festivals
    merged_events = {}
    for e in all_events:
        key = (e["date"], e["festival_name"])

        if key not in merged_events:
            merged_events[key] = e
        else:
            # Same festival found in another calendar
            merged_events[key]["calendar"] = "merged"

    final_events = sorted(
        merged_events.values(),
        key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d")
    )
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(final_events, f, indent=4, ensure_ascii=False)
    except FileNotFoundError as e:
        print("File is Not Found")
        print(e)
    #print(f"{len(final_events)} merged festivals saved for {CURRENT_YEAR}")
