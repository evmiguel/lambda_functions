import boto3
from boto3.dynamodb.conditions import Attr

def create_dynamodb_client():
    client = boto3.resource('dynamodb')
    return client

def get_unapproved_consultations(payload):
    dynamodb = create_dynamodb_client()
    table = dynamodb.Table('consultations')
    response = table.scan(
        FilterExpression=Attr('approved').eq("no")
    )
    items = response['Items']
    return items

def lambda_handler(event,context):
    return get_unapproved_consultations(event)


if __name__ == "__main__":
    lambda_handler({},"context")