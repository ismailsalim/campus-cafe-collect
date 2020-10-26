import json
from botocore.exceptions import ClientError

from main.lambdautils.DecimalEncoder import DecimalEncoder
from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
from main.posobjects.BasePOS import BasePOS
from main.posobjects.OdooPOS import OdooPOS


class GetMenuHandler(BaseLambdaHandler):
    """
    handler to return the menu for a given venue
    """
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event: dict, context: dict) -> dict:
        table = self.db.getTable()

        try:
            response = table.get_item(
                Key={
                    'venueid': event["venueid"],
                    'typeid': event["typeid"],
                }
            )
        except ClientError as e:
            print("Couldn't fetch item from Venues table:", e)
            return {
                'statusCode': self.clientErrorCode
            }

        # get pos id from item
        pos_id = response['Item']['posid']
        creds = response['Item']['poscreds']

        pos = self.getPOSObject(pos_id, event["venueid"], creds)

        try:
            menu = pos.getMenu()
            data = {
                'statusCode': self.successCode,
                'body': json.dumps(menu, indent=4, cls=DecimalEncoder)
            }
            return data
        except Exception as e:
            print("Couldn't fetch menu for POS {} ; ".format(pos), e)
            return {
                'statusCode': self.clientErrorCode
            }

    def getPOSObject(self, pos_id: str, venue_id: str, creds: list) -> BasePOS:
        if pos_id == "Odoo":
            return OdooPOS(venue_id, creds)
        else:
            raise NotImplementedError("No object for POS type {} is available".format(pos_id))
