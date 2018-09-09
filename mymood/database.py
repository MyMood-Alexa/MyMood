
from interaction import Interaction
import boto3


boto3.setup_default_session(region_name='us-west-1')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Interactions')


def create_table():
    # Key1: sessionId from Alexa
    # Key2: Time from when the session started
    table = dynamodb.create_table(
        TableName='Interactions',
        KeySchema=[
            {
                'AttributeName': "sessionId",
                'KeyType': "HASH"

            },
            {
                'AttributeName': "time",
                'KeyType': "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': "sessionId",
                'AttributeType': "S"
            },
            {
                'AttributeName': "time",
                'AttributeType': "S"
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
        )
    print("Table status:", table.table_status)


def add_interaction(session_id, time, responses, device_id, user_id):
    # string, string, list, string
    table.put_item(
        Item={
            'sessionId': session_id,
            'time': time,
            'responses': responses,
            'deviceId': device_id,
            'userId': user_id
        }
    )


def update_responses(interaction):
    global table
    table.update_item(
        Key={
            'sessionId': interaction.session_id,
            'time': interaction.time
        },
        UpdateExpression="set responses = :r",
        ExpressionAttributeValues={
                ':r': interaction.responses,
        },
        ReturnValues="UPDATED_NEW"
        )


def get_all_interactions():
    interactions = []
    response = table.scan()

    for s in response['Items']:
        interaction = Interaction(s['sessionId'], s['time'], s['responses'],
                                  s['deviceId'], s['user_id'])
        interactions.append(interaction)

    return interactions
