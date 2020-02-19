from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('FoodTags')

    try:
        print("TABLE", table)
        response = table.get_item(
            Key={
                'foodtag': event['foodtag']
            }
        )
    except ClientError as e:
        return {
            'statusCode': 404
        }

    item = response['Item']
    count = item['count']

    if item:
        data = json.dumps(item, indent=4, cls=DecimalEncoder)
        return {
            'statusCode': 200,
            'body': count
        }

    else:
        return {
            'statusCode': 404
        }
