from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
import json


class GetVenueByPriceHandler(BaseLambdaHandler):
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event, context):
        table = self.db.getTable()
        price_rank = event["pricerank"]

        try:
            response = table.scan(
                FilterExpression=Attr("pricerank").eq(price_rank)
            )
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