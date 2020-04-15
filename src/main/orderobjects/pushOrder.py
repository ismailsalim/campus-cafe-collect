import json
from botocore.exceptions import ClientError
import stripe

from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
from main.lambdautils.miscellaneous import miscellaneous
from main.posobjects.OdooPOS import OdooPOS


class PushOrderHandler(BaseLambdaHandler):
    """
    handler to push and order for a given venue
    """

    def __init__(self, dbObject):
        super().__init__(dbObject)
        self.stripeKey = miscellaneous['stripeAPIkey']

    def handle_request(self, event: dict, context: dict) -> dict:
        data = event['body'].replace("'", "\"")
        data = json.loads(data)

        if not self.checkPaymentWasMade(data):
            return {
                'statusCode': self.clientErrorCode
            }

        table = self.db.getTable()

        venue_id = event["data"]["object"]["metadata"]["venueid"]
        type_id = event["data"]["object"]["metadata"]["typeid"]

        try:
            response = table.get_item(
                Key={
                    'venueid': venue_id,
                    'typeid': type_id,
                }
            )
        except ClientError as e:
            print("Couldn't fetch item from Venues table:", e)
            return {
                'statusCode': self.clientErrorCode
            }

        pos_id = response['Item']['posid']
        creds = response['Item']['poscreds']

        pos = self.getPOSObject(pos_id, event["venueid"], creds)

        try:
            receipt = pos.pushOrder(event)
        except ClientError as e:
            return {
                'statusCode': self.clientErrorCode
            }
        return {'statusCode': self.successCode,
                'body': json.dumps(receipt)}

    def checkPaymentWasMade(self, data: dict) -> bool:
        try:
            stripeEvent = stripe.Event.construct_from(data, self.stripeKey)
        except ValueError as e:
            return False
        if stripeEvent.type == 'checkout.session.completed':
            return True
        return False

    def getPOSObject(self, pos_id: str, venue_id: str, creds: list):
        if pos_id == "Odoo":
            return OdooPOS(venue_id, creds)
        else:
            raise NotImplementedError("No object for POS type {} is available".format(pos_id))
