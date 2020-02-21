from botocore.exceptions import ClientError
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
import json


class GetVenueHandler(BaseLambdaHandler):
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event, context):
        table = self.db.getTable()

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
                'statusCode': self.clientErrorCode
            }

        item = response['Item']

        # if fetched item is empty then return NOT FOUND error
        if item:

            return {
                'statusCode': self.successCode,
                'body': json.dumps(item, indent=4, cls=self.encoder)
            }
        else:
            return {
                'statusCode': self.clientErrorCode
            }