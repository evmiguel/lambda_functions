import boto3
import json
import string
import random
import requests
from datetime import datetime
from pytz import timezone

def create_dynamodb_client():
    client = boto3.resource('dynamodb')
    return client

def create_consultation(payload):
    dynamodb = create_dynamodb_client()
    table = dynamodb.Table('consultations')
    if 'rejected' in payload:
        delete_appointment(payload["order"],table)
        return { "message" : "Appointment has been rejected"}
    if 'approved' in payload and payload['approved'] == 'yes':
        update_table(payload["order"],payload["approved"],table)
        new_google_event(payload)
        return { "message": "Appointment has been approved." }
    data = {
            'name': payload['name'],
            'order': order_generator(),
            'e-mail': payload['e-mail'],
            'date': payload['date'],
            'start_time': payload['start_time'],
            'end_time': payload['end_time'],
            'time_zone': payload['time_zone'],
            'company': payload['company'],
            'message': payload['message'],
            'phone_number': payload['phone_number'],
            'approved': "no"
        }
    if 'end_date' in payload:
        data['end_date'] = payload['end_date']
    table.put_item(
        Item=data
    )
    return {"message": "Appointment has been created and is waiting for approval."}

def update_table(order,approved,table):
    table.update_item(
        Key={
            'order': order,
        },
        UpdateExpression='SET approved = :val',
        ExpressionAttributeValues={
            ':val': approved
        }
    )

def delete_appointment(order,table):
    table.delete_item(
        Key={
            'order': order
        }
    )

def new_google_event(data):
    url = "https://api.erikamiguel.com/consult/new-google-event"
    start_time_iso = get_iso_time(data['date'], data['start_time'], data['time_zone'])
    if 'end_date' in data:
        end_time_iso = get_iso_time(data['end_date'], data['end_time'], data['time_zone'])
    else:
        end_time_iso = get_iso_time(data['date'], data['end_time'], data['time_zone'])
    summary = "Chat Erika/"+data['name']+". Appointment ID: " + data['order']
    e_mail = str(data['e-mail'])
    body = {
        "summary": summary,
        "attendees": [
            { "email": e_mail }],
        "start": {
            "dateTime": start_time_iso,
        },
        "end": {
            "dateTime":  end_time_iso,
        }
    }
    json_data = json.dumps(body, ensure_ascii=False)
    r = requests.post(url,data=json_data)


def get_iso_time(date, time, time_zone):
    time_string = date + " " + time
    time_object = datetime.strptime(time_string, '%m/%d/%Y %I:%M%p')
    zone = timezone(time_zone)
    time_iso = zone.localize(time_object).isoformat("T")
    return str(time_iso)


def order_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def lambda_handler(event,context):
    create_consultation(event)


if __name__ == "__main__":
    lambda_handler({
  "date": "11/26/2016",
  "e-mail": "erika@erikamiguel.com",
  "end_time": "01:00AM",
  "name": "Erika Miguel",
  "order": "980OEWAYTA",
  "start_time": "11:00PM",
  "time_zone": "America/New_York",
},"context")
