# actual lambda function to be used for setting price ranks

from main.lambdautils.DBConnection import DynamoConn
from main.updatedbobjects.setPriceRank import SetPriceRankHandler


def lambda_handler(event, context):
    handler = SetPriceRankHandler(DynamoConn("Venues"))
    return handler.handle_request(event,context)
