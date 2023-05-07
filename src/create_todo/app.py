import boto3
import os
import json
import uuid
from datetime import datetime

def create(message, context):
    if ('body' not in message or message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    table_name = os.environ.get('TABLE', 'Todos')
    region = os.environ.get('REGION', 'eu-west-2')

    todo_table = boto3.resource('dynamodb', region_name=region)
    table = todo_table.Table(table_name)
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
        'headers': {},
        'body': json.dumps({'msg': 'New Todo Created'})
    }