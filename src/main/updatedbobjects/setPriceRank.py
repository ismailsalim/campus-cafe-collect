from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
from main.lambdautils.DBConnection import DynamoConn
from main.venueobjects.getVenues import GetVenuesHandler
from main.menuobjects.getMenu import GetMenuHandler

import json


class SetPriceRankHandler(BaseLambdaHandler):
    def __init__(self, dbOject):
        super().__init__(dbOject)

    def handle_request(self, event, context):

        response = self.getAllVenues()
        if response['statusCode'] == self.successCode:
            venues = json.loads(response['body'])
            # do something here if fails
        else:
            return {
                'statusCode': self.clientErrorCode,
            }

        table = self.db.getTable()
        for venue in venues:
            venue_id = venue['venueid']
            type_id = venue['typeid']
            input_params = {
                "venueid": venue_id,
                "typeid": type_id
            }
            # fetching the menu from a specific venue
            response = self.getMenuForVenue(input_params)

            if response['statusCode'] != self.successCode:
                return {
                    'statusCode': self.clientErrorCode,
                }  # log here

            menu = json.loads(response['body'])
            venue_prices = self.getPriceList(menu)
            price_rank = self.rankPriceList(venue_prices)

            # updating price attribute for each venue in venues
            table.update_item(
                Key={
                    'venueid': venue_id,
                    'typeid': type_id
                },
                UpdateExpression="set pricerank = :t",
                ExpressionAttributeValues={
                    ':t': price_rank
                }
            )

        return {
            'statusCode': self.successCode,
            'body': json.dumps('Price ranks set successfully!')
        }

    @staticmethod
    def rankPriceList(priceList):
        avgPrice = round(sum(priceList) / len(priceList), 2)
        print("Venue Average: ", avgPrice)
        rank = 3 if avgPrice >= 20 else (2 if avgPrice >= 10 else 1)
        return rank

    @staticmethod
    def getPriceList(menu):
        priecList = []
        for category in menu:
            items = menu[category]
            priecList += [float(item[1]) for item in items]
        print("Venue Price List:", priecList)
        return priecList

    @staticmethod
    def getAllVenues():
        conn = DynamoConn("Venues")  # will be used later on as well
        getVenuesHandler = GetVenuesHandler(conn)
        return getVenuesHandler.handle_request(event=None, context=None)

    @staticmethod
    def getMenuForVenue(params):
        getMenuHandler = GetMenuHandler(DynamoConn('Credentials'))
        return getMenuHandler.handle_request(event=params, context=None)
