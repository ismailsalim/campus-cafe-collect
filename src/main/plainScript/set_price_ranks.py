import json
import string
from datetime import datetime
import boto3
from boto3 import client as boto3_client
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    lambda_client = boto3_client('lambda')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    venues_table = dynamodb.Table('Venues')

    # fetch all the venue data
    response = lambda_client.invoke(FunctionName="get-venues", InvocationType='RequestResponse')
    payload = json.loads(response['Payload'].read().decode("utf-8"))

    body = payload['body']
    venues = json.loads(body)

    for venue in venues:
        venue_price = []

        venue_id = venue['venueid']
        type_id = venue['typeid']

        # print("VENUE ID = ", venue_id)
        # print("TYPE ID = ", type_id)
        # fetching the menu from a specific venue
        input_params = {
            "venueid": venue_id,
            "typeid": type_id
        }

        response = lambda_client.invoke(FunctionName="get-menu", InvocationType='RequestResponse',
                                        Payload=json.dumps(input_params))

        payload = json.loads(response['Payload'].read().decode("utf-8"))
        print(payload)
        body = payload['body']
        menu = json.loads(body)

        # generate tags associated with each venue
        for category in menu:
            items = menu[category]
            for item in items:
                prices = item[1]
                venue_price.append(prices)

        average_price = sum(venue_price) / len(venue_price)  # Should update this to ignore outliers etc
        print("Venue Price List:", venue_price)
        print("Venue Average: ", average_price)

        if 20 < average_price:  # Need to discuss what values these should
            price_rank = "3"
        elif 10 < average_price <= 20:
            price_rank = "2"
        else:
            price_rank = "1"

        # updating price attribute for each venue in venues
        venues_table.update_item(
            Key={
                'venueid': venue_id,
                'typeid': type_id
            },
            UpdateExpression="set pricerank = :t",
            ExpressionAttributeValues={
                ':t': price_rank
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Price ranks set successfully!')
    }