import json


def mask_text(text, visible_start=2, visible_end=2):
    if not text:
        return text

    text = str(text)

    if len(text) <= visible_start + visible_end:
        return "*" * len(text)

    return (
        text[:visible_start]
        + "*" * (len(text) - visible_start - visible_end)
        + text[-visible_end:]
    )


def mask_email(email):
    if not email or "@" not in email:
        return mask_text(email)

    username, domain = email.split("@", 1)

    if len(username) <= 2:
        username = "*" * len(username)
    else:
        username = username[:2] + "*" * (len(username) - 2)

    return f"{username}@{domain}"


DATA_FILE = "Data/data.json"

# Read data.json
with open(DATA_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# Mask sensitive fields
for record in data:
    if "Name" in record:
        record["Name"] = mask_text(record["Name"])

    if "Email address" in record:
        record["Email address"] = mask_email(record["Email address"])

    if "Responder Email Address" in record:
        record["Responder Email Address"] = mask_email(
            record["Responder Email Address"]
        )

    if "Birthdate" in record:
        birthdate = str(record["Birthdate"]).strip()

        if "/" in birthdate:
            year = birthdate.split("/")[-1]
        elif "-" in birthdate:
            year = birthdate.split("-")[0]  # Handles YYYY-MM-DD
        else:
            year = "****"

        record["Birthdate"] = f"**/**/{year}"

# Overwrite the same file
with open(DATA_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"{DATA_FILE} has been masked successfully.")