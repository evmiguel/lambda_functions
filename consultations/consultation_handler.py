import boto3
import time
import string
import random

def create_dynamodb_client():
    client = boto3.resource('dynamodb')
    return client

def create_consultation(payload):
    dynamodb = create_dynamodb_client()
    table = dynamodb.Table('consultations')
    id = create_id(table)
    table.put_item(
        Item={
            'id': id,
            'name': payload['name'],
            'order': order_generator(),
            'e-mail': payload['e-mail'],
            'date': payload['date'],
            'start_time': payload['start_time'],
            'end_time': payload['end_time']
        }
    )

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
            'name': '',
            'e-mail': '',
            'date': '',
            'start_time': '',
            'end_time': ''
        },"context")
