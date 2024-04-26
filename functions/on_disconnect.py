import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')

def generate_response(body_content, code: int = 200):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': "application/json"
        },
        'body': json.dumps(body_content)
    }

def handler(event, context):
    table_name = os.environ.get('TABLE_NAME')
    table = dynamodb.Table(table_name)

    try:
        table.delete_item(
            Key={
                'pk': event["requestContext"]["connectionId"],
                'sk': 'connectionId',
            }
        )
        return generate_response("Disconnected.", code=200)
    except Exception as e:
        print(e)
        return generate_response(e, code=500)