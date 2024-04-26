import boto3
import json
import os


bedrock_client = boto3.client('bedrock-runtime')

def generate_response(body_content = None, code: int = 200):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': "application/json"
        },
        'body': None if body_content is None else json.dumps(body_content)
    }

def handler(event, context):
    apigw_client = boto3.client('apigatewaymanagementapi', endpoint_url=f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}")

    prompt = json.loads(event['body'])['prompt']

    connection_id = event['requestContext']['connectionId']
    def reply(connection_id: str, content: str):
        apigw_client.post_to_connection(
            ConnectionId=connection_id,
            Data=content
        )


    model_id = "meta.llama3-8b-instruct-v1:0"
    try:
        response = bedrock_client.invoke_model_with_response_stream(
            modelId=model_id,
            body=json.dumps({
                'prompt': prompt,
                'max_gen_len': 1000,
                "temperature": 0.5
            }),
            accept='application/json', 
            contentType='application/json'
        )

        stream = response.get('body')

        if stream:
            for event in stream:
                chunk = event.get('chunk')
                if chunk:
                    chunk_obj = json.loads(chunk.get('bytes').decode())
                    generated_text = chunk_obj.get('generation')

                    reply(connection_id, generated_text)

        
        return generate_response({"status": "OK"})
    except Exception as e:
        print(e)
        return generate_response(e, code=500)