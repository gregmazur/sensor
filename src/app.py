import datetime
import json
import os
import boto3
import urllib3

print('Loading function')
region_name = os.environ['REGION_NAME']
dynamo = boto3.client('dynamodb', region_name=region_name)
table_name = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    print("!!!!!Received event: ")

    data = json.loads(event['body'])
    print(data)

    if 'temp1' not in data:
        raise Exception("No temp")
    timestamp = datetime.datetime.now().isoformat()

    http = urllib3.PoolManager()
    
    temperature = http.request('GET','http://api.openweathermap.org/data/2.5/weather?lat=46.478161&lon=30.714075&units=metric&appid=b48854bacc86e27e946f128132f23585')
    temperature = json.loads(temperature.data)['main']

    item = {
        'timestamp': {'S': timestamp },
        'temp1': {'S': str(data['temp1'])},
        'hum1': {'S': str(data['hum1'])},
        'light': {'S': str(data['light'])},
        'outTemp': {'S': str(temperature['temp'])},
        'outHum': {'S': str(temperature['humidity'])},
        'outPressure': {'S': str(temperature['pressure'])}
    }

    dynamo.put_item(TableName=table_name,Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response