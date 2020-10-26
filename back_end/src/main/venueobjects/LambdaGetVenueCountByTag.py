# actual lambda function to be used for getting venue counts

from main.venueobjects.getVenueCountByTag import GetVenueCountByTagHandler
from main.lambdautils.DBConnection import DynamoConn


def lambda_handler(event, context):
    handler = GetVenueCountByTagHandler(DynamoConn("FoodTags"))
    return handler.handle_request(event, context)
