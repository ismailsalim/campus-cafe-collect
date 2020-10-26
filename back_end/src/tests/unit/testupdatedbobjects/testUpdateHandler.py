from unittest import TestCase
from unittest.mock import Mock, patch
from main.updatedbobjects.UpdateHandler import UpdateHandler


# we define a derived Mock class that has a 'scan' method, which cannot be easily mocked otherwise
class ScanableMock(Mock):
    def __init__(self, scanReturnVal):
        super().__init__()
        self.scanReturnVal = scanReturnVal

    def scan(self, **kwargs):
        return self.scanReturnVal

class TestUpdateHandler(TestCase):

    def setUp(self) -> None:
        self.getVenuesMethod = UpdateHandler.getAllVenues
        self.getMenuMethod = UpdateHandler.getMenuForVenue

    @patch('main.menuobjects.getMenu.GetMenuHandler.handle_request')
    def testCallsGetMenuHandlerWhenGetsMenu(self, mockedMethod):
        self.getMenuMethod({'dummy': 1})
        self.assertTrue(mockedMethod.called)

    @patch('main.lambdautils.DBConnection.DynamoConn.getTable',
           return_value=ScanableMock({'Items': ['venue1', 'venue2']}))
    def testGetsAllMenusIfConnectionOK(self, mockedMethod):
        expected = ['venue1', 'venue2']
        self.assertEqual(self.getVenuesMethod(), expected)

    @patch('main.lambdautils.DBConnection.DynamoConn.getTable', return_value=ScanableMock('NonSubscriptableObject'))
    def testReturnsEmptyIfCannotGetConnectionForVenues(self, mockedMethod):
        expected = []
        self.assertEqual(self.getVenuesMethod(), expected)
