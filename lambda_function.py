import boto3
import json
from anthropic import Anthropic
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "PROD-ANTHROPIC-API-KEY"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])['ANTHROPIC_API_KEY']
    client.close()
    return secret

secret_key = get_secret()

client = Anthropic(
    api_key=(secret_key),
)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('first_table')


def lambda_handler(event, context):

    # create a claude session
    message = client.messages.create(
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-sonnet-4-20250514",
    )
    message_input_cost = round(message.usage.input_tokens * 0.0003, 5)
    message_output_cost = round(message.usage.output_tokens * 0.0015, 5)
    # get response text
    claude_response = message.content[0].text
    
    #create response to send to user
    response = {
        "statusCode": 200,
        "body": json.dumps({ 
            "input_tokens": message.usage.input_tokens,
            "message_input_cost_cents": message_input_cost,
            "output_tokens": message.usage.output_tokens,
            "message_output_cost_cents": message_output_cost,
            "claude_response": claude_response,
        }),
    }

    # write response data to DDB table
    ddb_item = {
        'LambdaRequestID': context.aws_request_id,
        'response_status': response['statusCode'],
        'response_text': claude_response,
        'input_tokens': message.usage.input_tokens,
        'output_tokens': message.usage.output_tokens,
    }

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('first_table')
    table.put_item(Item=ddb_item)

    return response
