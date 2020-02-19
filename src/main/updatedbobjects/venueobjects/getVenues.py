from botocore.exceptions import ClientError
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
import json


class GetVenuesHandler(BaseLambdaHandler):
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event, context):
        table = self.db.getTable()

        try:
            response = table.scan()
        except ClientError as e:
            return {
                'statusCode': self.clientErrorCode
            }

        venues = response['Items']

        if venues:
            return {
                'statusCode': self.successCode,
                'body': json.dumps(venues, indent=4, cls=self.encoder)
            }

        else:
            return {
                'statusCode': self.clientErrorCode
            }