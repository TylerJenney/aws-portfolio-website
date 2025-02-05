import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WebsiteVisitors')  

def lambda_handler(event, context):
    try:
        # Retrieve the current visitor count
        response = table.get_item(Key={'id': 'visitorcounter'})
        count = response.get('Item', {}).get('count', 0)

        # Convert Decimal to int before using it
        count = int(count)

        # Increment count
        count += 1
        table.put_item(Item={'id': 'visitorcounter', 'count': count})

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'visitorCount': count})
        }

    except Exception as e:
        print(f"Error: {str(e)}")  # Logs the error in CloudWatch
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }