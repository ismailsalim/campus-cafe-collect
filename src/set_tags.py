import json
import string
from datetime import datetime
from collections import Counter
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

    print("PAYLOAD", payload)

    body = payload['body']
    venues = json.loads(body)

    tags_and_counts = {}
    tags_and_venues = {}

    for venue in venues:
        venue_tags = set()

        venue_id = venue['venueid']
        type_id = venue['typeid']

        # fetching the menu from a specific venue
        input_params = {
            "venueid": venue_id,
            "typeid": type_id
        }
        print("CALLING GET MENU")
        response = lambda_client.invoke(FunctionName="get-menu", InvocationType='RequestResponse',
                                        Payload=json.dumps(input_params))

        payload = json.loads(response['Payload'].read().decode("utf-8"))

        print("PAYLOAD 2", payload)
        body = payload['body']
        menu = json.loads(body)

        # generate tags associated with each venue
        for category in menu:
            items = menu[category]
            for item in items:
                tags = item[0].lower().split()
                venue_tags.update(tags)

        final_venue_tags = process_tags(list(venue_tags))

        add_to_tags_counts(final_venue_tags, tags_and_counts)

        add_to_tags_venues(final_venue_tags, venue_id, type_id, tags_and_venues)

        print("")
        print("VENUE TAG SET", final_venue_tags)
        print("")
        # updating tags attribute for each venue in venues
        venues_table.update_item(
            Key={
                'venueid': venue_id,
                'typeid': type_id
            },
            UpdateExpression="set tags = :t",
            ExpressionAttributeValues={
                ':t': final_venue_tags
            }
        )

    tag_table = dynamodb.Table('FoodTags')
    # NOTE: Each list item in venues will be a list [venue_id, type]
    for (t1, count), (t2, venues) in zip(tags_and_counts.items(), tags_and_venues.items()):
        tag_table.put_item(
            TableName='FoodTags',
            Item={
                'foodtag': t1,
                'count': count,
                'venues': venues
            }
        )

    print("")
    print("FINAL TAG and COUNTS", tags_and_counts)
    print("FINAL TAG and VENUES", tags_and_venues)
    print("")

    return {
        'statusCode': 200,
    }


def process_tags(tags_list):
    # removes digits
    tags_list = [x for x in tags_list if not any(x1.isdigit() for x1 in x)]

    # removes punctuation
    punctuation = string.punctuation.replace("-", "")  # preserve hyphenated words
    tags_list = [''.join(c for c in t if c not in punctuation) for t in tags_list]

    # remove tags of length less than two
    tags_list = [t for t in tags_list if len(t) > 2]

    return tags_list


def add_to_tags_counts(tags, tags_and_counts):
    for tag in tags:
        if not tag in tags_and_counts:
            tags_and_counts[tag] = 1
        else:
            tags_and_counts[tag] += 1


def add_to_tags_venues(tags, venue, type_id, tags_and_venues):
    for tag in tags:
        if not tag in tags_and_venues:
            tags_and_venues[tag] = [[venue, type_id]]
        else:
            tags_and_venues[tag].append([venue, type_id])