import boto3
import datetime

boto3.setup_default_session(region_name='us-west-1') 
dynamodb = boto3.resource("dynamodb") 
table = dynamodb.Table("Interactions")
date = datetime.date.today()

def create_table():
    #Key1: sessionId from Alexa
    #Key2: Time from when the session started
    table = dynamodb.create_table(
        TableName='Interactions',
        KeySchema=[
            {
                'AttributeName': 'sessionId',
                'KeyType': 'HASH'
                        
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'sessionId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
        )
    print("Table status:", table.table_status)
    
create_table();
def add_responses(sessionId, time, responses):
    #string, string, list
    table.put_item(
        Item={
            "sessionId": sessionId,
            "time": time,
            "responses": responses,
        }
    )
    

def update_responses(sessionId, time, responses):
    table.update_item(
        Key={
                "sessionId": sessionId,
                "time": time
            },
        UpdateExpression="set responses = :r",
        ExpressionAttributeValues={
                ":r": responses,
            },
        ReturnValues="UPDATED_NEW"
        )