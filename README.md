# 📧 Email Bot - Automated Email Sending System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)
[![SMTP](https://img.shields.io/badge/SMTP-Protocol-FF6B6B?style=for-the-badge)](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)
[![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-API-34A853?style=for-the-badge&logo=google-sheets)](https://developers.google.com/sheets/api)
[![Gmail](https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](https://mail.google.com)

**🤖 Intelligent Automated Email Delivery System with Google Sheets Integration**

[Features](#-features) • [Getting Started](#-getting-started) • [Project Structure](#-project-structure) • [Configuration](#-configuration) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

---

## 📱 Overview

**Email Bot** is a sophisticated Python-based automation system that seamlessly integrates with Google Sheets to manage and send personalized emails. The system intelligently handles **Birthday wishes**, **Festival greetings**, **Welcome emails**, and **Scheduled custom messages** with template support, secure delivery, and simplified communication management.

### ✨ Key Highlights
- 🎂 **Automatic Birthday Reminders** - Never miss a birthday again!
- 🎉 **Festival Greetings** - Send festival wishes automatically
- 👋 **Welcome Emails** - Personalized welcome messages for new users
- 📅 **Scheduled Messages** - Custom emails on specific dates
- 🔒 **Secure Email Validation** - Domain & MX record verification
- 📊 **Google Sheets Sync** - Centralized recipient management
- 📝 **Template Support** - Beautiful HTML email templates
- 📈 **Activity Logging** - Comprehensive system logs & statistics
- 🎨 **Colorful Console Output** - Interactive terminal feedback

---

## 🚀 Features

### Core Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| 📊 **Google Sheets Integration** | Fetch recipient data from Google Sheets | ✅ Active |
| 🎂 **Birthday Automation** | Send birthday greetings on configured dates | ✅ Active |
| 🎊 **Festival Notifications** | Automated festival wishes distribution | ✅ Active |
| 📧 **HTML Email Templates** | Customizable email templates with placeholders | ✅ Active |
| 🔐 **Email Validation** | DNS/MX record verification for email addresses | ✅ Active |
| 📋 **Activity Tracking** | Log all sent emails and system activities | ✅ Active |
| ⚙️ **Environment Configuration** | Secure credentials management via .env | ✅ Active |
| 🛡️ **Error Handling** | Comprehensive exception handling & logging | ✅ Active |

---

## 📋 Tech Stack

### Languages & Frameworks
![Python](https://img.shields.io/badge/Python-3.8+-3670A0?style=flat-square&logo=python&logoColor=ffdd54)

### Key Libraries
```
📦 python-dotenv      - Environment variable management
📦 colorama           - Colorful terminal output
📦 dnspython          - DNS resolution for email validation
📦 google-auth        - Google authentication
📦 google-api-python-client - Google Sheets API integration
```

### Services & APIs
- 🟢 **Google Sheets API** - Data source management
- 📧 **Gmail SMTP** - Email delivery (smtp.gmail.com:465)
- 🔐 **Google OAuth 2.0** - Secure authentication

---

## 📁 Project Structure

```
email-bot/
├── 📄 task01.py                 # Daily automation task (Birthdays & Festivals)
├── 📄 task02.py                 # Additional email tasks
├── 📄 service.py                # Core service module (Email, Auth, Utils)
├── 📄 requirements.txt          # Python dependencies
├── 📄 .gitignore                # Git ignore rules
│
├── 📁 Module/                   # Utility modules
│   ├── setup_logger.py          # Logging configuration
│   ├── calendar.py              # Festival & birthday filtering
│   └── google_sheet.py          # Google Sheets operations
│
├── 📁 Template/                 # HTML email templates
│   ├── Birthday_Wishing_Mail.html
│   ├── Festival_Mail.html
│   ├── Thank_You_Mail.html
│   └── Two_Factor_Authentication.html
│
├── 📁 Data/                     # Data storage
│   ├── data.json                # Recipients database
│   └── festivals.json           # Festival calendar
│
├── 📁 Logs/                     # System logs
│   └── email_bot.log            # Application logs
│
└── 📁 Secure/                   # Configuration (⚠️ Not in repo)
    ├── credentials.json         # Google Sheet credential file
    └── .env                     # Environment variables
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Account with Sheets API enabled
- Gmail Account (for SMTP)
- Git

### Step 1️⃣: Clone the Repository

```bash
git clone https://github.com/mairhythmhoon/email-bot.git
cd email-bot
```

### Step 2️⃣: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3️⃣: Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Sheets API** and **Google Drive API**
4. Create OAuth 2.0 credentials (Service Account)
5. Download the JSON credentials file
6. Place it in the `Secure/` directory

### Step 4️⃣: Environment Configuration

Create a `.env` file in the `Secure/` directory:

```env
# Gmail Configuration
E_MAIL=your-email@gmail.com
PASSWORD=your-app-specific-password
RESPONS_MAILE=your-reply-to@gmail.com

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
```

**⚠️ Important:** Generate an [App-Specific Password](https://support.google.com/accounts/answer/185833) for Gmail if you have 2FA enabled.

### Step 5️⃣: Prepare Data Files

#### `Data/data.json`
```json
[
    {
        "Name": "John Doe",
        "Email address": "john@example.com",
        "Birthdate": "15/03/1995"
    },
    {
        "Name": "Jane Smith",
        "Email address": "jane@example.com",
        "Birthdate": "22/08/1998"
    }
]
```

#### `Data/festivals.json`
```json
[
    {
        "festival_name": "New Year",
        "date": "01/01/2026"
    },
    {
        "festival_name": "Diwali",
        "date": "01/11/2026"
    }
]
```

---

## 🚀 Usage

### Run Daily Automation Task

```bash
python task01.py
```

This will:
- 🔍 Fetch recipient data from Google Sheets
- 🎂 Check for birthdays and send wishes
- 🎉 Check for festivals and send greetings
- 📊 Log activities to Google Sheets
- 📝 Generate system logs

### Run Additional Tasks

```bash
python task02.py
```

### Schedule Automated Runs

#### On Linux/Mac (using cron):
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 8 AM
0 8 * * * cd /path/to/email-bot && python task01.py
```

#### On Windows (using Task Scheduler):
1. Open **Task Scheduler**
2. Create a new task
3. Set trigger: Daily at 8:00 AM
4. Set action: Execute `python.exe` with argument `C:\path\to\task01.py`

---

## 📧 Email Templates

The system supports customizable HTML email templates with dynamic placeholders:

- `{name}` - Recipient's name
- `{festival}` - Festival name

### Example Template Structure
```html
<html>
  <body>
    <h1>Hello {name}! 🎉</h1>
    <p>Wishing you a wonderful {festival}!</p>
  </body>
</html>
```

---

## 🔐 Security & Best Practices

### Credential Management
- ✅ Use environment variables (`.env` file)
- ✅ Never commit `.env` to Git
- ✅ Use Gmail App-Specific Passwords (not your main password)
- ✅ Keep credentials.json private

### Email Validation
- ✅ Regex pattern validation
- ✅ MX record verification
- ✅ Domain existence checking
- ✅ Automatic error logging

### Error Handling
- ✅ Comprehensive try-catch blocks
- ✅ Detailed logging system
- ✅ Graceful failure recovery

---

## 📊 Activity Tracking

### Logged Metrics
- 📈 Total emails sent
- 🎂 Birthday emails count
- 🎉 Festival emails count
- ❌ Failed delivery attempts
- ⏰ Execution timestamps

### Output Logs
```
[2026-04-24 08:30:15] INFO: EMAIL SYSTEM STARTED
[2026-04-24 08:30:16] INFO: Fetching Data From Database
[2026-04-24 08:30:18] INFO: Birthday Today: John Doe
[2026-04-24 08:30:20] INFO: Email sent to john@example.com
[2026-04-24 08:30:21] INFO: EMAIL SYSTEM ENDED
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Gmail authentication fails** | Ensure App-Specific Password is used, not your main password |
| **Invalid email format error** | Check email format in `data.json` |
| **MX record lookup fails** | Verify internet connection, domain may not exist |
| **Google Sheets not syncing** | Verify credentials.json and API permissions |
| **Templates not loading** | Ensure template files exist in `Template/` directory |
| **No emails sent** | Check if dates in `data.json` match today's date |

---

## 📝 Logging & Debugging

View detailed logs in `Logs/email_bot.log`:

```bash
# View last 20 lines
tail -20 Logs/email_bot.log

# Watch logs in real-time
tail -f Logs/email_bot.log
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Contribution
- 📧 Additional email templates
- 🎨 Enhanced HTML designs
- 🌍 Internationalization (multi-language support)
- ⚡ Performance optimizations
- 📱 SMS notification support

---

## 📚 Documentation

### Module Details

**`service.py`** - Core service module
- Email sending functionality (SMTP)
- Template loading and management
- Email validation with DNS lookup
- Google Sheets integration
- Logging and activity tracking

**`task01.py`** - Daily automation task
- Birthday checking and filtering
- Festival notification logic
- Statistics generation
- Google Sheets data sync

**`task02.py`** - Additional email operations
- Custom scheduled emails
- Bulk email sending
- User management tasks

---

## 📞 Contact & Support

### Get in Touch
- **GitHub:** [@mairhythmhoon](https://github.com/mairhythmhoon)
- **Email:** [rhythm.work.id@proton.me](mailto:rhythm.work.id@proton.me)
- **Instagram:** [@mairhythmhoon](https://instagram.com/mairhythmhoon)
- **LinkedIn:** [@mairhythmhoon](https://linkedin.com/in/mairhythmhoon)

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).<br><br>
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 💡 Future Enhancements

- Advanced scheduling with cron expressions
- Multi-language template support
- User preference management
- Automated email list segmentation

---

<div align="center">

### ⭐ If you found this project helpful, please consider giving it a star!

**Built with ❤️ by [mairhythmhoon](https://github.com/mairhythmhoon)**

---

[![](https://komarev.com/ghpvc/?username=mairhythmhoon&repo=email-bot&color=blueviolet&style=flat-square)](https://visitcount.itsvg.in)

*Last Updated: April 24, 2026*

</div>