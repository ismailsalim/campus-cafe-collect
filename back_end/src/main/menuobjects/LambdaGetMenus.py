# actual lambda function to be used for getting menus

from main.menuobjects.getMenu import GetMenuHandler
from main.lambdautils.DBConnection import DynamoConn


def lambda_handler(event, context):
    handler = GetMenuHandler(DynamoConn("Credentials"))
    return handler.handle_request(event, context)
