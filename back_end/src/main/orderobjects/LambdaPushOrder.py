# actual lambda function to be used for pushing orders

from main.orderobjects.pushOrder import PushOrderHandler
from main.lambdautils.DBConnection import DynamoConn
from main.lambdautils.ConfirmationEmail import ConfirmationEmail


def lambda_handler(event, context):
    handler = PushOrderHandler(DynamoConn('Credentials'))
    response = handler.handle_request(event, context)
    email = ConfirmationEmail(event['body'], handler.customerEmail)
    if response['statusCode'] == handler.successCode:
        email.sendConfirmation()

    return response
