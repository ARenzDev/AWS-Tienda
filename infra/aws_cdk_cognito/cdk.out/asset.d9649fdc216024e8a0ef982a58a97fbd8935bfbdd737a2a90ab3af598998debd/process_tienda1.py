import json

def lambda_handler(event, context):
    print("Eventos recibidos para tienda1:")
    for record in event.get('Records', []):
        detail = json.loads(record['detail'])
        print(f"Procesando registro de tienda1: {detail}")
    return {"statusCode": 200, "body": "Evento de tienda1 procesado"}