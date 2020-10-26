# actual lambda function to be used for setting tags

from main.lambdautils.DBConnection import DynamoConn
from main.updatedbobjects.setTags import SetTagsHandler


def lambda_handler(event, context):
    handler = SetTagsHandler(DynamoConn("Venues"))
    return handler.handle_request(event, context)
