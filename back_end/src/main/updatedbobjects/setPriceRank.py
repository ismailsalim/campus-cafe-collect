from main.updatedbobjects.UpdateHandler import UpdateHandler

import json


class SetPriceRankHandler(UpdateHandler):
    """
    handler to set a price rank for a given venue given its prices on the menu
    """

    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event: object, context: object) -> dict:

        venues = self.getAllVenues()
        if len(venues) == 0:
            return {'statusCode': self.clientErrorCode}
        table = self.db.getTable()

        for venue in venues:
            venue_id = venue['venueid']
            type_id = venue['typeid']

            getMenu_input_params = {
                "venueid": venue_id,
                "typeid": type_id
            }
            # fetching the menu from a specific venue
            response = self.getMenuForVenue(getMenu_input_params)

            if response['statusCode'] != self.successCode:
                return {
                    'statusCode': self.clientErrorCode,
                }

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
                    ':t': str(price_rank)
                }
            )

        return {
            'statusCode': self.successCode,
            'body': json.dumps('Price ranks set successfully!')
        }

    @staticmethod
    def rankPriceList(priceList: list) -> int:
        avgPrice = round(sum(priceList) / len(priceList), 2)
        print("Venue Average: ", avgPrice)
        rank = 3 if avgPrice >= 20 else (2 if avgPrice >= 10 else 1)
        return rank

    @staticmethod
    def getPriceList(menu: dict) -> list:
        priecList = []
        for category in menu:
            items = menu[category]
            priecList += [float(item[1]) for item in items]
        print("Venue Price List:", priecList)
        return priecList

