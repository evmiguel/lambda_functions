from oauth2client import client
from oauth2client.client import OAuth2Credentials
from googleapiclient import discovery
import boto3
import json
import httplib2
import datetime

def get_credential():
    client = boto3.client('s3')
    client.download_file('your-bucket-name','credentials.json','/tmp/credentials.json')
    data = ""
    with open('/tmp/credentials.json') as data_file:    
        data = data_file.read()
    creds = OAuth2Credentials.from_json(data)
    http_auth = creds.authorize(httplib2.Http())
    return http_auth

def create_event(event):
    print event
    auth = get_credential()
    service = discovery.build('calendar', 'v3', http=auth)
    event = service.events().insert(calendarId='your-calendar-id', body=event,sendNotifications=True).execute()
    print 'Event created: %s' % (event.get('htmlLink'))
    
def lambda_handler(event, context):
    create_event(event)


if __name__ == "__main__":
    lambda_handler({
        'summary': 'test event',
        'start': {
            'dateTime': '2016-11-08T19:43:38-00:00',
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': '2016-11-08T20:44:19-00:00',
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': 'erika@erikamiguel.com'},
        ]}, "context")



