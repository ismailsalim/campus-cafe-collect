from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
import json


class GetVenueCountByTagHandler(BaseLambdaHandler):
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event, context):
        table = self.db.getTable()

        try:
            response = table.get_item(
                Key={
                    'foodtag': event['foodtag']
                }
            )
        except ClientError as e:
            return {
                'statusCode': self.clientErrorCode
            }

        venue = response['Item']
        count = venue['count']

        if venue:
            data = json.dumps(venue, indent=4, cls=self.encoder)
            return {
                'statusCode': self.successCode,
                'body': count
            }

        else:
            return {
                'statusCode': self.clientErrorCode
            }