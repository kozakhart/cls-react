
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil import parser
import datetime
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

def main():
    dirname = os.path.dirname(__file__)
    SERVICE_ACCOUNT_FILE = os.path.join(dirname, 'opi-calendar-key.json')

    credentials = service_account.Credentials.from_service_account_file(filename=SERVICE_ACCOUNT_FILE)

    service = build('calendar', 'v3', credentials=credentials)

    Calendar_ID = 'byuopi@gmail.com'

    current_datetime = datetime.now().astimezone(timezone.utc)
    time_adjustment = timedelta(minutes=1)
    current_date_rfc3339 = (current_datetime - time_adjustment).isoformat()

    events = service.events().list(calendarId=Calendar_ID, singleEvents=True,maxResults=2500, timeMin=current_date_rfc3339).execute()
    list = []
    dic = {}
    for any_event in events['items']:
        if "Center Closed" in any_event['summary']:
            if 'date' in any_event['start']:
                # All-day event
                start_date = any_event['start']['date']
                parsed_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%m-%d-%Y')
                print(f"Center Closed all-day event start date: {parsed_date}")
                dic = {'Event':any_event['summary'], 'Date':parsed_date}
            elif 'dateTime' in any_event['start']:
                # Timed event
                start_datetime = any_event['start']['dateTime']
                parsed_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S%z')
                start_date = parsed_datetime.strftime('%m-%d-%Y')
                start_time = parsed_datetime.strftime('%H:%M')
                print(f"Center Closed timed event start date: {start_date}")
                dic = {'Event':any_event['summary'], 'Date':start_date}
            else:
                print("Center Closed event has no start date or time.")
                print(any_event['summary'])
            list.append(dic)

    base_path = Path(__file__).parent
    file_path = (base_path / "events.json").resolve()
    with open(file_path, "w") as outfile:
        jsonString = json.dumps(list)
        outfile.write(jsonString)
        outfile.close()

def check_booths(test_date, test_time, language, record_number):
    dirname = os.path.dirname(__file__)
    SERVICE_ACCOUNT_FILE = os.path.join(dirname, 'opi-calendar-key.json')
    credentials = service_account.Credentials.from_service_account_file(filename=SERVICE_ACCOUNT_FILE)
    service = build('calendar', 'v3', credentials=credentials)
    Calendar_ID = 'byuopi@gmail.com'
    events = service.events().list(calendarId=Calendar_ID).execute()
    print(f"Test date: {test_date}")
    print(f"Test time: {test_time}")
    unavailable_booths = []
    for any_event in events['items']:
        if "Booth" in any_event['summary']:
            if 'dateTime' in any_event['start']:
                start_datetime = any_event['start']['dateTime']
                parsed_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S%z')
                start_date = parsed_datetime.strftime('%m/%d/%Y')
                start_time = parsed_datetime.strftime('%H:%M')
                print(f"Booth event summary: {any_event['summary']}")
                #print(f'Booth description: {any_event["description"]}')
                print(f"Booth event start date: {start_date}")
                print(f"Booth event start time: {start_time}")
                if str(start_date) == test_date and str(start_time) == test_time:
                    parts = any_event['summary'].split()
                    print(parts[1])
                    booth_number = int(parts[1].replace("-", ""))
                    unavailable_booths.append(booth_number)
                else:
                    print("Booth event is not at the same time as the test event.")
            else:
                print("Booth event has no start date or time.")
    print(f"Unavailable booths- {unavailable_booths}")
    if len(unavailable_booths) == 0:
        assigned_booth = 1
        schedule_booth(test_date, test_time, assigned_booth, language, record_number)
    elif 6 not in unavailable_booths:
        assigned_booth = max(unavailable_booths) + 1
        schedule_booth(test_date, test_time, assigned_booth, language, record_number)
    else:
        assigned_booth = "No booths available."
    print(f"Your booth is- {assigned_booth}")

def schedule_booth(test_date, test_time, booth_number, language, record_number):
    from datetime import datetime, timedelta
    dirname = os.path.dirname(__file__)
    SERVICE_ACCOUNT_FILE = os.path.join(dirname, 'opi-calendar-key.json')
    credentials = service_account.Credentials.from_service_account_file(filename=SERVICE_ACCOUNT_FILE)
    service = build('calendar', 'v3', credentials=credentials)
    Calendar_ID = 'byuopi@gmail.com'

    test_date = datetime.strptime(test_date, '%m/%d/%Y')
    test_time = datetime.strptime(test_time, '%H:%M')
    combined_datetime = datetime(test_date.year, test_date.month, test_date.day, test_time.hour, test_time.minute)
    formatted_datetime = combined_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    test_time_plus_30 = test_time + timedelta(minutes=30)
    combined_datetime_plus_30 = datetime(test_date.year, test_date.month, test_date.day, test_time_plus_30.hour, test_time_plus_30.minute)
    formatted_datetime_plus_30 = combined_datetime_plus_30.strftime('%Y-%m-%dT%H:%M:%S')
    event_data = {
    'summary': f'Booth {str(booth_number)}- {language}',
    'description': f'Record {str(record_number)}',
    'start': {
        'dateTime': f'{formatted_datetime}',
        'timeZone': 'America/Denver',
    },
    'end': {
        'dateTime': f'{formatted_datetime_plus_30}',
        'timeZone': 'America/Denver',
    },
    }

# Create the event
    event = service.events().insert(calendarId=Calendar_ID, body=event_data).execute()

# Print the event details
    print('Event created: %s' % (event.get('htmlLink')))

#check_booths('09/13/2023', '16:30', 'German', '12345')
