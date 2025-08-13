import boto3
import json
from uuid import uuid4
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
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    
    secret = json.loads(get_secret_value_response['SecretString'])['ANTHROPIC_API_KEY']
    client.close()
    return secret



def get_message_history(conversation_id, table):
    message_history = table.get_item(Key={"conversation_id":conversation_id})
    return message_history["Item"]["messages"]

# create anthropic session
client = Anthropic(
    api_key=(get_secret()),
)

def lambda_handler(event, context):

    conversation_id = event.get("conversation_id")
    message_history = []

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('message-history')

    if conversation_id == None:
        conversation_id = f"{uuid4()}"
    else:
        message_history = get_message_history(conversation_id, table)
    
    new_message = {"role": "user", "content": event["message"]}
    message_history.append(new_message)
    # create a claude session
    message = client.messages.create(
        max_tokens = 1024,
        messages = message_history,
        model = "claude-sonnet-4-20250514",
    )

    # get response text
    claude_response = message.content[0].text
    
    claude_message = {
    "role": message.role,
    "content": claude_response
    }

    message_history.append(claude_message)

    #create response to send to user
    response = {
        "conversation_id": conversation_id,
        "body": claude_response,
        
    }

    # write response data to DDB table
    ddb_item = {
        "conversation_id": conversation_id,
        "messages": message_history 
    }

    table.put_item(Item=ddb_item)
    return response
