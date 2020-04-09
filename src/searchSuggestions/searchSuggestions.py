from __future__ import print_function # Python 2/3 compatibility
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

    query = event['query']

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('FoodTags')
    
    queries = query.lower().split()
    
    # Only searching for first 3 query terms
    # STUPID WAY OF DOING THIS BUT QUICK BUG FIX
    response = 0
    if len(queries) == 1:
        fe1 = Attr('foodtag').contains(queries[0])
        try:
            response = table.scan(
                FilterExpression=fe1
        )
        except ClientError as e:
            return {
                'statusCode' : 404
            }
    
    if len(queries) == 2:
        print("GETS HERE")
        fe1 = Attr('foodtag').contains(queries[0])
        fe2 = Attr('foodtag').contains(queries[1])
        try:
            response = table.scan(
                FilterExpression= (fe1 | fe2)
            )
        except ClientError as e:
            return {
                'statusCode' : 404
            }

    if len(queries) >= 3:
        fe1 = Attr('foodtag').contains(queries[0])
        fe2 = Attr('foodtag').contains(queries[1])
        fe3 = Attr('foodtag').contains(queries[2])

        try:
            response = table.scan(
            FilterExpression=(fe1 | fe2 | fe3)
            )
        except ClientError as e:
            return {
                'statusCode' : 404
            }
    

    # Use response from scanning foodtags table to then return count to front-end
    items = response['Items']
    
    if items:
        tags_and_counts = []
        
        for item in items:
            tag_and_count = (item["foodtag"], int(item["count"]))
            tags_and_counts.append(tag_and_count)
    
        data = json.dumps(tags_and_counts, indent=4, cls=DecimalEncoder)
        return {
            'statusCode' : 200,
            'body' : data
        }
        
    else:
        return {
            'statusCode' : 404
        }
