import boto3
import os
import json
from datetime import datetime

table_name = os.environ.get('TABLE', 'Todos')
region = os.environ.get('REGION', 'eu-west-2')
dynamo_db = boto3.resource('dynamodb', region_name=region)

def delete(message, context):
    if ('pathParameters' not in message or message['httpMethod'] != 'DELETE'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    
    table = dynamo_db.Table(table_name)
    todo_id = message['pathParameters']['id']

    params = {
        'id': todo_id
    }
    
    response = table.delete_item(
        Key=params
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : '*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials' : True,
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'msg': 'Todo Deleted'})
    }