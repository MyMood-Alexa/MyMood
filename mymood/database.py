import boto3
import datetime

boto3.setup_default_session(region_name='us-west-1') 
dynamodb = boto3.resource("dynamodb") 
table = dynamodb.Table("Interactions")
date = datetime.date.today()

def create_table():
    #TODO need key to differentiate users
    table = dynamodb.create_table(
        TableName='Interactions',
        KeySchema=[
            {
                'AttributeName': 'date',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'date',
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
    
    
def add_responses(time, responses):
    #string, string, list
    table.put_item(
        Item={
            "date": str(date),
            "time": time,
            "responses": responses,
        }
    )
    

def update_responses(time, responses):
    table.update_item(
        Key={
                "date": str(date),
                "time": time
            },
        UpdateExpression="set responses = :r",
        ExpressionAttributeValues={
                ":r": responses,
            },
        ReturnValues="UPDATED_NEW"
        )