from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


## Should take in tags, return ENTIRE row in Venues table
## Should take in search term, return ENTIRE row in Venues table
## Should take in user latitude/longitude and radius, returns ENTIRE row within this range in Venues table

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
    price_min = event['pricemin']
    price_max = event['pricemax']
    loc_long = event['longitude']
    loc_lat = event['latitude']
    print("LOC LANG", type(loc_long))
    loc_radius = event['radius']
    min_long, max_long, min_lat, max_lat = convert_km_to_degrees(loc_long, loc_lat, loc_radius)

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

        queries = query.lower().split()

        if query_matched(queries, name.lower(), tags):
            venues_dict[venue_id] = type_id

    items = []

    # split pricerank into list (can move above)
    # price_ranks = price_rank_str.split(",")

    for venue in venues_dict:
        venue_id = venue
        type_id = venues_dict[venue_id]

        # for price_rank in range(price_min, price_max + 1):
        print("MINLONG", decimal.Decimal(min_long))
        print("MAXLONG", decimal.Decimal(max_long))
        print("MINLAT", decimal.Decimal(min_lat))
        print("MAXLAT", decimal.Decimal(max_lat))
        response = table.scan(
            FilterExpression=(Attr("venueid").eq(venue_id) &
                              Attr("typeid").eq(type_id) &
                              Attr("pricerank").between(price_min, price_max) &
                              # Attr("latitude").between(decimal.Decimal(str(51.500609)),decimal.Decimal(str(51.500619))))
                              Attr("longitude").between(decimal.Decimal(str(min_long)),
                                                        decimal.Decimal(str(max_long))) &
                              Attr("latitude").between(decimal.Decimal(str(min_lat)), decimal.Decimal(str(max_lat)))
                              )
        )
        item = response['Items']
        if item:
            items.append(item)

    print("ITEMTEMEMEMEME: ", items)

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
    if not queries:
        return True
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


import math


def convert_km_to_degrees(longitude, latitude, radius):
    radius_deg_lat = radius / 110.54
    radius_deg_long = radius / (11.320 * math.cos(radius_deg_lat))

    min_long = longitude - radius_deg_long
    max_long = longitude + radius_deg_long

    min_lat = latitude - radius_deg_lat
    max_lat = latitude + radius_deg_lat

    return min_long, max_long, min_lat, max_lat

