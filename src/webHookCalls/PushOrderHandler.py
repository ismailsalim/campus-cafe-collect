import json
from botocore.exceptions import ClientError

from BaseLambdaHandler import BaseLambdaHandler
from OdooPOS import OdooPOS


class PushOrderHandler(BaseLambdaHandler):
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event, context):
        table = self.db.getTable()
        
        venue_id = event["data"]["object"]["metadata"]["venueid"]
        type_id = '1'
        #type_id = event[ids[0]]['typeid']

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

        pos = self.getPOSObject(pos_id, venue_id, creds)

        try:
            items = event["data"]["object"]["display_items"]
            receipt = pos.pushOrder(items)
        except ClientError as e:
            return {
                'statusCode':self.clientErrorCode
            }
        print(receipt)
        return  {'statusCode':self.successCode,
                'body':json.dumps(receipt)}


    def getPOSObject(self, pos_id, venue_id, creds):
        if pos_id == "Odoo":
            return OdooPOS(venue_id, creds)
        else:
            raise NotImplementedError("No object for POS type {} is available".format(pos_id))