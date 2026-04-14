from datetime import datetime, timedelta
import json
import logging
logger = logging.getLogger(__name__)

def birthday_filter(bday_data):
    today = datetime.today().date()
    next15 = today + timedelta(days=15)

    bdays = []

    for p in bday_data:
        b = datetime.strptime(p["Birthdate"], "%d/%m/%Y").date()
        b_this = b.replace(year=today.year)

        if b_this < today:
            b_this = b_this.replace(year=today.year + 1)

        bdays.append({
            "name": p["Name"],
            "email": p["Email address"],
            "date": b_this
        })

    bdays.sort(key=lambda x: x["date"])

    next15_bday = [b for b in bdays if today < b["date"] <= next15]
    future_bday = [b for b in bdays if b["date"] > today]

    if next15_bday:
        return next15_bday
    elif future_bday:
        return [future_bday[0]]
    else:
        return []

def festival_filter(fest_data):
    today = datetime.today().date()
    next15 = today + timedelta(days=15)

    fests = []

    for f in fest_data:
        d = datetime.strptime(f["date"], "%Y-%m-%d").date()
        if d >= today:
            fests.append({
                "name": f["festival_name"],
                "date": d
            })

    fests.sort(key=lambda x: x["date"])

    next15_fest = [f for f in fests if today < f["date"] <= next15]
    future_fest = [f for f in fests if f["date"] > today]

    if next15_fest:
        result = next15_fest.copy()
        return result
    elif future_fest:
        return [future_fest[0]]
    else:
        return []
    
# this is for only dry run
if __name__ == "__main__":

    with open(f"/home/kali/email-bot/Data/data.json", "r", encoding="utf-8") as f:
        bday_data = json.load(f)

    with open(f"/home/kali/email-bot/Data/festivals.json", "r", encoding="utf-8") as f:
        fest_data = json.load(f)

    a = birthday_filter(bday_data)
    b = festival_filter(fest_data)
    
    bday_content = ""
    for item in a:
        #print("Name:", item["name"],"| Email:", item["email"],"| Date:", item["date"])
        bday_content += f" • {item['name']} ({item['email']}) - {item['date']}\n"
    print("\n")
    
    fest_content = ""
    for item in b:
        #print("Festival:", item["name"],"| Date:", item["date"])
        fest_content+= f" • {item['name']} - {item['date']}\n"

    print(bday_content)
    print(fest_content)
