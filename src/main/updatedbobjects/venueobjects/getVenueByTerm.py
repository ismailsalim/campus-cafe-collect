from botocore.exceptions import ClientError
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
import json


class GetVenueByTermHandler(BaseLambdaHandler):
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event, context):
        table = self.db.getTable()
        query = event['query']

        try:
            response = table.scan()

        except ClientError as e:
            return {
                'statusCode': self.clientErrorCode
            }

        venues = response['Items']

        venues_dict = {}

        for venue in venues:
            tags = venue['tags']
            name = venue['name']

            venue_id = venue['venueid']
            type_id = venue['typeid']

            queries = query.lower().split()

            if self.query_matched(queries, name.lower(), tags):
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
            data = json.dumps(items, indent=4, cls=self.encoder)
            return {
                'statusCode': 200,
                'body': items
            }

        else:
            return {
                'statusCode': 404
            }

    def query_matched(self, queries, name, tags):
        return self.tag_matched(queries, tags) or self.name_matched(queries, name)

    def name_matched(self, queries, name):
        for query in queries:
            if query in name:
                return True
        return False

    def tag_matched(self, queries, tags):
        for tag in tags:
            for query in queries:
                if query in tag:
                    return True
        return False
