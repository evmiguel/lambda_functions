import boto3
from datetime import datetime
import string
import random

def create_dynamodb_client():
    client = boto3.resource('dynamodb')
    return client

def create_message(payload):
    dynamodb = create_dynamodb_client()
    table = dynamodb.Table('guestbook')
    date = get_date()
    data = {
            'name': payload['name'],
            'message': payload['message'],
            'date' : date,
            'order': order_generator()
        }
    table.put_item(
        Item=data
    )
    return { "message" : "Guestbook message created" }

def get_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")

def lambda_handler(event,context):
    create_message(event)

def order_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == "__main__":
    lambda_handler({
  "name": "Erika Miguel",
  "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam quis libero facilisis erat ornare aliquet. Proin pharetra auctor dictum."
},"context")
