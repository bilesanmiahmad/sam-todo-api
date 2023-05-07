import boto3
import os
import json
from datetime import datetime

def update(message, context):
    if ('pathParameters' not in message or message['httpMethod'] != 'PUT'):
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
    todo_id = message['pathParameters']['id']

    params = {
        'id': todo_id
    }
    
    response = table.update_item(
        Key=params,
        UpdateExpression="set title = :s, description = :s, isDone = :s",
        ExpressionAttributeValues={
            ":s": activity['title'],
            ":s": activity['description'],
            ":s": activity['isDone']
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'Todo Updated'})
    }