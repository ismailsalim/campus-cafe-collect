from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
import json


class GetVenueCountByTagHandler(BaseLambdaHandler):
    """
    handler that returns venues by food tags count
    """

    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event: dict, context: dict) -> dict:
        table = self.db.getTable()

        queries = event['query'].lower().split()
        count = min(3, len(queries))

        # tricky to pass arbitrary number of expressions into FilterExpression
        # one option to loop through the possible queries (up to 3)
        results = []
        for i in range(count):
            try:
                response = table.scan(
                    FilterExpression=Attr('foodtag').contains(queries[i])
                )
            except ClientError as e:
                return {
                    'statusCode': self.clientErrorCode
                }
            if response:
                results += response['Items']

        if results:
            tags_and_counts = []

            for item in results:
                tag_and_count = (item["foodtag"], int(item["count"]))
                tags_and_counts.append(tag_and_count)
            data = json.dumps(tags_and_counts, indent=4, cls=self.encoder)
            return {
                'statusCode': self.successCode,
                'body': data
            }

        else:
            return {
                'statusCode': self.clientErrorCode
            }
