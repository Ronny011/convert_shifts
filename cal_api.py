from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# read/write access to the calendar
# if modifying these scopes, delete the file token.pickle (if exists)
scopes = ['https://www.googleapis.com/auth/calendar']
# client secret file, downloaded from the google cloud console (oauth credentials)
client_secret = 'client_secret.json'


def import_df(subject, start_date, start_time, end_date, end_time):
    """
    calls the google calendar api to insert events from DataFrame
    :param subject: event name
    :param start_date: event start date
    :param start_time: event start time
    :param end_date: event end date
    :param end_time: event end time
    """
    creds = None  # credentials
    # token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time. we need to check it's existence before using it
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        # if there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # if there are no credentials at all
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret, scopes)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    # single event json format
    event = {
        # event name
        'summary': subject,
        'location': 'HaKishon St. 18, Yavne, Israel',
        'start': {
            # single string for date and time: 'yyyy-mm-ddThh:mm:ss' with optionally adding '-hh:mm' as a UTC offset
            'dateTime': start_date + 'T' + start_time + ':00',
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': end_date + 'T' + end_time + ':00',
            'timeZone': 'Asia/Jerusalem',
        },
        'reminders': {
            'useDefault': True,
        },
    }
    print(event)
    # insert single event to the calendar
    #event = service.events().insert(calendarId='primary', body=event).execute() - use only when you want to insert events
    # print event URL
    #print('Event created: %s' % (event.get('htmlLink')))- use only when you want to insert events
