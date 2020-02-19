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
    table = dynamodb.Table('Venues')

    print("ABOUT TO GET ITEMS FROM TABLE")

    print("Scanning:")

    price_rank = event["pricerank"]

    response = table.scan(
        FilterExpression=Attr("pricerank").eq(price_rank)
    )
    data = response['Items']

    return {
        'statusCode': 200,
        'body': json.dumps(data, cls=DecimalEncoder)
    }
