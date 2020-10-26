from unittest import TestCase
from unittest.mock import Mock
import json

from main.venueobjects.getVenues import GetVenuesHandler

GENERIC_VENUE = {'typeid': "1", "tags": ["bun", "water", "chips"], "name": "Buns", "venueid": "2"}


class TestGetVenuesHandler(TestCase):
    def setUp(self) -> None:
        self.dbObject = SubscriptMock()
        self.handler = GetVenuesHandler(self.dbObject)
        self.testData = {
            "query": "",
            "pricemin": 0,
            "pricemax": 3,
            "latitude": 51.498317,
            "longitude": -0.177243,
            "radius": 5,
            "restaurants": "true",
            "bars": "false",
            "cafes": "false"
        }


    def testExecutesNormalCase(self):
        expected = {'statusCode': self.handler.successCode,
                    'body': json.dumps([GENERIC_VENUE], indent=4, cls=self.handler.encoder)}
        self.assertTrue(expected, self.handler.handle_request(self.testData, {}))

    def testReturnsErrorCodeWhenNoDataIsReturned(self):
        expected = {'body': [], 'statusCode': 201}
        self.dbObject.getTable().scan().__getitem__ = Mock(side_effect=[{}])
        self.assertEqual(expected, self.handler.handle_request(self.testData, {}))

    def testConvertsKmToDegreesCorrectly(self):
        long = 1
        lat = 1
        radius = 5
        expectedResult = (0.9550775993512438, 1.044922400648756, 0.954995499549955, 1.045004500450045)
        actualResult = self.handler.convertKmToDegrees(long, lat, radius)
        self.assertTupleEqual(expectedResult, actualResult)

    def testGetsCorrectTypes(self):
        case1 = [True, False, False]
        expected1 = ["1"]
        case2 = [False, False, False]
        expected2 = ["1", "2", "3"]
        case3 = [False, True, True]
        expected3 = ["2", "3"]
        self.assertEqual(self.handler.getTypes(*case1), expected1)
        self.assertEqual(self.handler.getTypes(*case2), expected2)
        self.assertEqual(self.handler.getTypes(*case3), expected3)

    def testMatchesNamesCorrectly(self):
        query1 = []
        name1 = "test"

        query2 = ['ab', 'can', 'burger']
        name2 = "lobster burger"

        query3 = ['n', 'fish']
        name3 = "spaghetti"

        self.assertTrue(self.handler.nameMatched(query1, name1))
        self.assertTrue(self.handler.nameMatched(query2, name2))
        self.assertFalse(self.handler.nameMatched(query3, name3))

    def testMatchesTagsCorrectly(self):
        tags1 = ['abc', 'bcd', 'cde', 'ufo']
        query1 = ['ab', 'e']
        tags2 = ['abc', 'bcd', 'cde', 'ufo']
        query2 = ['z', 'xy']
        self.assertTrue(self.handler.tagMatched(query1, tags1))
        self.assertFalse(self.handler.tagMatched(query2, tags2))

    def testMatchesQueriesCorrectly(self):
        query1 = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
        tags1 = ['fox', 'rabbit', 'brown']
        name1 = "imperial college caffe"
        query2 = ['lorem', 'ipsum']
        tags2 = ['something', 'random']
        name2 = "honest burgers"
        self.assertTrue(self.handler.queryMatched(query1, name1, tags1))
        self.assertFalse(self.handler.queryMatched(query2, name2, tags2))


class SubscriptMock(Mock):  # need a subscriptable mock, need to think about how to not set posid to Odoo only
    def __getitem__(self, item) -> list:
        return [GENERIC_VENUE]
