import boto3
import os
import json

table_name = os.environ.get('TABLE', 'Todos')
region = os.environ.get('REGION', 'eu-west-2')
dynamo_db = boto3.resource('dynamodb', region_name=region)

def list(message, context):
    if ('httpMethod' not in message or message['httpMethod'] != 'GET'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    
    table = dynamo_db.Table(table_name)
    
    response = table.scan()
    print(response)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : '*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials' : True,
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response['Items'])
    }