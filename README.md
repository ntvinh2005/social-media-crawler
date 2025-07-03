# Facebook Feed Scraper (Automatically Login)

This tool uses Selenium to log in to Facebook automatically with email/phone and password or with a test account chrome profile (consider config it in server),
search for keywords, scroll the feed like a human, click "See More" ("Xem thêm"),
and scrape post content, likes, and comments.

## Features
- Automatic login 
- Human-like typing and scrolling
- Scrapes page names, content, emoji counts, and comment counts
- Supports Vietnamese Facebook layout (I need to check to see the different in UI layout in different region later using VPN and other test account)

## Requirements

- Python 3.9 or later
- Google Chrome installed
- ChromeDriver matching your Chrome version: https://chromedriver.chromium.org/downloads

## Installation

```bash
pip install selenium
```

## 🛠️ Setup

1. **Clone or download this repo**.
2. Open `main.py` and edit your search keywords or login method.

## Auto Login (Test Accounts Only)

Replace these two lines in the .env file with your credentials:

```.env
PHONE_NUMBER = "YOUR_PHONE_NUMBER"
PASSWORD = "YOUR_PASSWORD"
```

Note: Auto login may trigger Facebook security checks. 

## How to Run

```bash
python main.py
```

The script will:
- Log you in (automatically) (type each letter slowly)
- Search one of several random whiskey-related queries 
- Scroll the feed one post at a time
- Click "Xem thêm" when available
- Print post data (title, content, likes, comments)

  Note: The account I use to test right now have password leaked in a data breach so the script might be interupt by Chrome alert. Just turn it off to continue testing or reset password.

## Output

Currently the output is printed to terminal. 

## Notes

- The script assumes the interface is in **Vietnamese** for detecting "Xem thêm" and "bình luận".
- Make sure Chrome is **not already running** if using a custom profile.
