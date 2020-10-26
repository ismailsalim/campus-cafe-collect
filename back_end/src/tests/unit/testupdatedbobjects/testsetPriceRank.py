from unittest import TestCase
from unittest.mock import Mock, patch
import json

from main.updatedbobjects.setPriceRank import SetPriceRankHandler

class TestSetPriceRank(TestCase):
    def setUp(self) -> None:
        self.mockDB = Mock()
        self.handler = SetPriceRankHandler(self.mockDB)
        self.genericPriceList = [12, 16, 19, 20, 15.4, 0.99, 100]
        self.genericPriceListRank = 3
        self.menu = {
            'first': [('a', '1'), ('a', '1'), ('a', '1')],
            'second': [('b', '2'), ('b', '2'), ('b', '2')],
            'third': [('c', '3'), ('c', '3'), ('c', '3')]
        }
        self.priceListFromMenu = [1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0]
        self.successCase = {'statusCode': self.handler.successCode,
                            'body': json.dumps('Price ranks set successfully!')}
        self.failCase = {'statusCode': self.handler.clientErrorCode}

    MOCKGETVENUESRESULT = [{'venueid': '1', 'typeid': '1'}, {'venueid': '2', 'typeid': '2'}]

    MOCKFAILVENUEGETRESULT = []

    MOCKFAILMENUGETRESULT = {'statusCode': 404}

    MOCKGETMENURESULT = {'statusCode': 200,
                         'body': json.dumps({
                             'categ1': [('itemOne', '1.0')],
                             'categ2': [('itemTwo', '2.5')],
                             'categ3': [('itemThree', '6.9')]
                         })}

    def testRanksPriceListCorrectly(self):
        self.assertEqual(self.genericPriceListRank, self.handler.rankPriceList(self.genericPriceList))

    def testConvertsToFloat(self):
        self.assertEqual(self.priceListFromMenu, self.handler.getPriceList(self.menu))

    @patch('main.updatedbobjects.setPriceRank.SetPriceRankHandler.getAllVenues', return_value=MOCKGETVENUESRESULT)
    @patch('main.updatedbobjects.setPriceRank.SetPriceRankHandler.getMenuForVenue', return_value=MOCKGETMENURESULT)
    def testProcessesEvent(self, mockVenueMethod, mockMenuMethod):
        self.assertEqual(self.successCase, self.handler.handle_request(None, None))

    @patch('main.updatedbobjects.setPriceRank.SetPriceRankHandler.getAllVenues', return_value=MOCKFAILVENUEGETRESULT)
    def testReturnsErrorCodeIfCannotGetVenues(self, mockVenueMethod):
        self.assertEqual(self.failCase, self.handler.handle_request(None, None))

    @patch('main.updatedbobjects.setPriceRank.SetPriceRankHandler.getAllVenues', return_value=MOCKGETVENUESRESULT)
    @patch('main.updatedbobjects.setPriceRank.SetPriceRankHandler.getMenuForVenue', return_value=MOCKFAILMENUGETRESULT)
    def testReturnsErrorCodeIfCannotGetMenu(self, mockMenuMethod, mockVenueMethod):
        self.assertEqual(self.failCase, self.handler.handle_request(None, None))
