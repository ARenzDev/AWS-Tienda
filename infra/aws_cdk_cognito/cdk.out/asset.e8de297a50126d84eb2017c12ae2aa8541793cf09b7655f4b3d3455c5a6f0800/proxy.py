import json
import boto3
import os

eventbridge = boto3.client('events')

def lambda_handler(event, context):
    try:
        # Parsear datos de la solicitud
        body = json.loads(event.get('body', '{}'))
        headers = event.get('headers', {})
        
        # Preparar detalles del evento
        event_detail = {
            "headers": headers,
            "body": body
        }

        # Enviar evento a EventBridge
        response = eventbridge.put_events(
            Entries=[
                {
                    'Source': 'custom.api.proxy',
                    'DetailType': 'API Request',
                    'Detail': json.dumps(event_detail),
                    'EventBusName': 'MyCustomEventBus'
                }
            ]
        )
        
        # Responder a API Gateway
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Evento enviado a EventBridge",
                "eventId": response['Entries'][0]['EventId']
            })
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Ocurrió un error al procesar la solicitud",
                "error": str(e)
            })
        }

  