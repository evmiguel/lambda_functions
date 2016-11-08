import boto3
import time
import string
import random
import requests
from datetime import datetime

def create_dynamodb_client():
    client = boto3.resource('dynamodb')
    return client

def create_consultation(payload):
    dynamodb = create_dynamodb_client()
    table = dynamodb.Table('consultations')
    id = create_id(table)
    data = {
            'id': id,
            'name': payload['name'],
            'order': order_generator(),
            'e-mail': payload['e-mail'],
            'date': payload['date'],
            'start_time': payload['start_time'],
            'end_time': payload['end_time']
        }
   # table.put_item(
   #     Item=data
   # )
    new_google_event(data)

def new_google_event(data):
    url = "https://api.erikamiguel.com/consult/new-google-event"
    start_time_iso = get_iso_time(data['date'], data['start_time'])
    end_time_iso = get_iso_time(data['date'], data['end_time'])
    summary = "Consultation with Erika. Order ID: " + data['order']
    e_mail = data['e-mail']
    print start_time_iso
    body = {
        "summary": summary,
        "attendees": [
            { "email": e_mail }],
        "start": {
            "dateTime": start_time_iso,
            "timeZone": "America/New_York"
        },
        "end": {
            "dateTime":  end_time_iso,
            "timeZone": "America/New_York"
        }
    }



    r = requests.post(url,data=body)
    print(r.status_code, r.reason)

def get_iso_time(date, time):
    time_string = date + " " + time
    time_object = datetime.strptime(time_string, '%Y-%m-%dT%I:%M%pZ')
    return time_object

def get_latest_id(table):
    response = table.get_item(
        Key={
            'id': 1,
            'name': 'latest_id'
        }
    )
    item = response['Item']['latest']
    return item

def create_id(table):
    id = get_latest_id(table)
    latest_id = id+1
    update_latest_id(latest_id,table)
    return latest_id


def update_latest_id(new_id,table):
    table.update_item(
        Key={
            'id': 1,
            'name': 'latest_id'
        },
        UpdateExpression='SET latest = :val',
        ExpressionAttributeValues={
            ':val': new_id
        }
    )

def order_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def lambda_handler(event,context):
    create_consultation(event)


if __name__ == "__main__":
    lambda_handler({
            'name': 'erika',
            'e-mail': 'erika@erikamiguel',
            'date': '11/10/2016',
            'start_time': '9:00PM',
            'end_time': '10:00PM'
        },"context")
