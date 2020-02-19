# ---------------------------------------------------------------------
# RETURNS THE APPROPRIATE VENUE ITEM FROM THE VENUES TABLE GIVEN A
# VENUE ID AND TYPE ID

# LAST EDITED: 03/02/2020
# ---------------------------------------------------------------------

from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


class DecimalEncoder(json.JSONEncoder):
    """Format JSON decimals appropriately"""

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('Venues')

    # try to fetch the item from the VENUES table
    try:
        response = table.get_item(
            Key={
                'venueid': event["venueid"],
                'typeid': event["typeid"]
            }
        )
    except ClientError as e:
        return {
            'statusCode': 404
        }

    item = response['Item']

    # if fetched item is empty then return NOT FOUND error
    if item:
        data = json.dumps(item, indent=4, cls=DecimalEncoder)
        return {
            'statusCode': 200,
            'body': data
        }

    else:
        return {
            'statusCode': 404
        }
