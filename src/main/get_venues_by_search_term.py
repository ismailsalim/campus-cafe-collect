from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


## Should take in tags, return ENTIRE row in Venues table
## Should take in search term, return ENTIRE row in Venues table
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('Venues')

    query = event['query']

    try:
        print("TABLE", table)

        # response = table.scan(
        #     FilterExpression=Attr("name").contains(query)
        # )

        response = table.scan()

    except ClientError as e:
        return {
            'statusCode': 404
        }

    venues = response['Items']

    venues_dict = {}

    for venue in venues:
        tags = venue['tags']
        name = venue['name']

        venue_id = venue['venueid']
        type_id = venue['typeid']

        queries = query.lower().split()  # Move out of the for-loop

        if query_matched(queries, name.lower(), tags):
            venues_dict[venue_id] = type_id

    items = []

    for venue in venues_dict:
        venue_id = venue
        type_id = venues_dict[venue_id]

        response = table.get_item(
            Key={
                'venueid': venue_id,
                'typeid': type_id
            }
        )
        item = response['Item']
        items.append(item)

    print(items)

    if items:
        data = json.dumps(items, indent=4, cls=DecimalEncoder)
        return {
            'statusCode': 200,
            'body': items
        }

    else:
        return {
            'statusCode': 404
        }


def query_matched(queries, name, tags):
    return tag_matched(queries, tags) or name_matched(queries, name)


def name_matched(queries, name):
    for query in queries:
        if query in name:
            return True
    return False


def tag_matched(queries, tags):
    for tag in tags:
        for query in queries:
            if query in tag:
                return True
    return False
