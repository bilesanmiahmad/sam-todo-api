import boto3
import os
import json
import uuid
from datetime import datetime

table_name = os.environ.get('TABLE', 'Todos')
region = os.environ.get('REGION', 'eu-west-2')
dynamo_db = boto3.resource('dynamodb', region_name=region)

def create(message, context):
    if ('body' not in message or message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table = dynamo_db.Table(table_name)
    activity = json.loads(message['body'])

    params = {
        'id': str(uuid.uuid4()),
        'title': activity['title'],
        'description': activity['description'],
        'isDone': activity['isDone'],
        'dateCreated': str(datetime.timestamp(datetime.now()))
    }

    response = table.put_item(TableName=table_name, Item=params)
    print(response)

    return {
        'statusCode': 201,
        'headers': {
            "Access-Control-Allow-Origin" : '*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials' : True,
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'msg': 'New Todo Created'})
    }