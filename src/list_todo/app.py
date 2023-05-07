import boto3
import os
import json

def list(message, context):
    if ('httpMethod' not in message or message['httpMethod'] != 'GET'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    table_name = os.environ.get('TABLE', 'Todos')
    region = os.environ.get('REGION', 'eu-west-2')

    todo_table = boto3.resource('dynamodb', region_name=region)
    table = todo_table.Table(table_name)
    
    response = table.scan()
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }