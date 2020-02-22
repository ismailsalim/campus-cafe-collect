from botocore.exceptions import ClientError
from unittest import TestCase
from unittest.mock import MagicMock, Mock
import json

from main.venueobjects.getVenues import GetVenuesHandler


class TestGetVenuesHandler(TestCase):
    def setUp(self) -> None:
        self.testData = {'Items': [{'typeID': '1', 'priceRank': '1'}]}
        self.dbObject = MagicMock()
        self.dbObject.getTable().scan().__getitem__ = Mock(side_effect=self.testData['Items'])
        self.handler = GetVenuesHandler(self.dbObject)
        self.errorCase = {'statusCode': self.handler.clientErrorCode}
        self.successCase = {'statusCode': self.handler.successCode,
                            'body': json.dumps(self.testData['Items'][0], indent=4, cls=self.handler.encoder)}

    def testExecutesNormalCase(self):
        self.assertEqual(self.successCase, self.handler.handle_request(None, None))

    def testReturnsErrorCodeWhenNoDataIsReturned(self):
        self.dbObject.getTable().scan().__getitem__ = Mock(side_effect=[{}])
        self.assertEqual(self.errorCase, self.handler.handle_request(None, None))
