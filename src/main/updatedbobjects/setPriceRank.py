from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
from main.lambdautils.DBConnection import DynamoConn
from main.venueobjects.getVenues import GetVenuesHandler
from main.menuobjects.getMenu import GetMenuHandler

import json


class SetPriceRankHandler(BaseLambdaHandler):
    def __init__(self, dbOject):
        super().__init__(dbOject)

    def handle_request(self, event, context):
        venuesConn = DynamoConn("Venues")
        getVenueHandler = GetVenuesHandler(venuesConn)  # creating an object to return all venues

        credentialsConn = DynamoConn('Credentials')
        getMenuHandler = GetMenuHandler(credentialsConn)

        response = getVenueHandler.handle_request(event=None, context=None)
        if response['statusCode'] == self.successCode:
            venues = json.loads(response['body'])
            # do something here if fails
        else:
            raise RuntimeError("Could not fetch all venues")

        table = self.db.getTable()
        for venue in venues:
            venue_id = venue['venueid']
            type_id = venue['typeid']
            input_params = {
                "venueid": venue_id,
                "typeid": type_id
            }
            # fetching the menu from a specific venue
            response = getMenuHandler.handle_request(event=input_params,context=None)

            if response['statusCode'] != self.successCode:
                continue  # log here

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
