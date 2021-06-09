from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

'''
Configuring credentials
'''
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
        if flags else tools.run(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))\

'''
Creates events
'''
def createEvent(eventSummary, eventStartDate, eventEndDate):
    EVENT = {
    'summary': eventSummary,
    'start': {'date': eventStartDate},
    'end':   {'date': eventEndDate},
    }

    e = CAL.events().insert(calendarId='primary',sendNotifications=False, body=EVENT).execute()
    print('''*** %s event added:
            Start: %s
            End: %s''' % (e['summary'].encode('utf-8'),
                e['start']['date'], e['end']['date']))

'''
Removes events
'''
def removeEvents():
    page_token = None
    while True:
        events = CAL.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            print("Removing event:", "\"" + event['summary'] + "\"")
            CAL.events().delete(calendarId='primary', eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break

'''
============ Main ============
'''
f = open('events.json')
data = json.load(f)
f.close()

removeEvents()

for (k, v) in data.items():
  createEvent(v,k,k)