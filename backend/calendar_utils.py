from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import timedelta
import os
from dotenv import load_dotenv
import dateparser
import json

# Load environment variables 
load_dotenv()
CALENDAR_ID = os.getenv("CALENDAR_ID")

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load JSON from environment variable
service_account_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

# Use the correct function for a dict, not a file
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES
)

# ✅ Build the service object (MISSING in your version)
service = build('calendar', 'v3', credentials=credentials)

def check_availability(date_time_str):
    dt = dateparser.parse(date_time_str)
    if not dt:
        return f"Error: Could not parse datetime from '{date_time_str}'"
    
    end = dt + timedelta(minutes=30)
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=dt.isoformat() + 'Z',
        timeMax=end.isoformat() + 'Z',
        singleEvents=True
    ).execute()

    events = events_result.get('items', [])
    return "Available" if not events else "Not Available"

def create_event(title, date_time_str, description=""):
    dt = dateparser.parse(date_time_str)
    if not dt:
        return f"Error: Could not parse datetime from '{date_time_str}'"

    end = dt + timedelta(minutes=30)
    event = {
        'summary': title,
        'description': description,
        'start': {'dateTime': dt.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
    }
    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"Event '{title}' booked on {dt.strftime('%A, %d %B %Y at %I:%M %p')}"
