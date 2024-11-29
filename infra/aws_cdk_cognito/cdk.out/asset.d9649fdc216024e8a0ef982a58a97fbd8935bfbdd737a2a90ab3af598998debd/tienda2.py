import json
import boto3
import os

eventbridge = boto3.client('events')

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('tienda2')
    # fruit_data = {
    #     "id": "A001",
    #     "type": "Manzana",
    #     "quantity": 50
    # }
    
    try:
        response = table.scan()
        items = response['Items']
        response = eventbridge.put_events(
        Entries=[
                {
                    'Source': 'tienda2.registration',
                    'DetailType': 'Productos2 registrado',
                    'Detail': json.dumps(items),
                    'EventBusName': os.environ['EVENT_BUS_NAME']
                }
            ]
        )

        # Manejo de paginación si hay más elementos
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },     
            'body': json.dumps(items)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },     
            'body': json.dumps({'error': str(e)})
        }
    
