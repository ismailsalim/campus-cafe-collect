# actual lambda function to be used for getting venues by price, location, tags,..

from main.venueobjects.getVenues import GetVenuesHandler
from main.lambdautils.DBConnection import DynamoConn


def lambda_handler(event, context):
    handler = GetVenuesHandler(DynamoConn("Venues"))
    return handler.handle_request(event, context)
