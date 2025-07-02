from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

# Load environment variables 
openai_key = os.getenv("OPENAI_API_KEY")

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'creds/service_account.json'
CALENDAR_ID = 'a264be16f15252fab75343a4c8c0dc550b4629b8149617203a26d61f45c79e98@group.calendar.google.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)

def check_availability(date_time_str):
    dt = datetime.fromisoformat(date_time_str)
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
    dt = datetime.fromisoformat(date_time_str)
    end = dt + timedelta(minutes=30)
    event = {
        'summary': title,
        'description': description,
        'start': {'dateTime': dt.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
    }
    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"Event '{title}' booked on {date_time_str}"
