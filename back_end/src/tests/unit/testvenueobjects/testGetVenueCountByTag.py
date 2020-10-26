from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch
from main.venueobjects.getVenueCountByTag import GetVenueCountByTagHandler
import json


class TestGetVenueCountByTagHandler(TestCase):
    def setUp(self) -> None:
        self.dbObject = MagicMock()
        self.handler = GetVenueCountByTagHandler(self.dbObject)
        self.genericEvent = {'query': 'can'}

    def testReturnsErrorWhenNoDataReturnedFromDb(self):
        expected = {'statusCode': self.handler.clientErrorCode}
        self.dbObject.getTable().scan = Mock(return_value=[])
        self.assertEqual(expected, self.handler.handle_request(self.genericEvent, {}))

    def testProcessesNormalCase(self):
        returnValue = {'Items': [{'foodtag': ['can', 'bun'], 'count': "2"}]}
        expected = {'statusCode': self.handler.successCode,
                    'body': json.dumps([(['can', 'bun'], 2)], indent=4, cls=self.handler.encoder)}
        self.dbObject.getTable().scan = Mock(return_value=returnValue)
        self.assertEqual(expected, self.handler.handle_request(self.genericEvent, {}))
