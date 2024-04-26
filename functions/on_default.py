import boto3
import json
import os


def generate_response(body_content, code: int = 200):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': "application/json"
        },
        'body': json.dumps(body_content)
    }

def handler(event, context):
    apigw_client = boto3.client('apigatewaymanagementapi', endpoint_url=f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}")

    try:
        apigw_client.post_to_connection(
            ConnectionId=event['requestContext']['connectionId'],
            Data='Use the sendmessage route to send a message. Example payload: {\"action\": \"sendmessage\", \"prompt\": \"What is the meaning of life?\"}'
        )
        return generate_response("Connected.", code=200)
    except Exception as e:
        print(e)
        return generate_response(e, code=500)