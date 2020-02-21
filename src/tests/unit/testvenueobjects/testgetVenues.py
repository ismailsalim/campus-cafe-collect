from unittest import TestCase
from unittest.mock import patch
from main.venueobjects.getVenue import GetVenueHandler
from main.lambdautils.DBConnection import DynamoConn


class TestGetVenue(TestCase):
    @patch('main.lambdautils.DBConnection.DynamoConn')
    def setUp(self, mockConn) -> None:
        self.handler = GetVenueHandler(mockConn())
