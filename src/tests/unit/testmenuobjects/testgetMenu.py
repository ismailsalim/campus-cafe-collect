from unittest import TestCase
from unittest.mock import Mock
from main.menuobjects.getMenu import GetMenuHandler


class TestGetMenu(TestCase):
    def setUp(self) -> None:
        self.mockDB = SubscriptMock()
        self.handler = GetMenuHandler(self.mockDB)
        self.OdooposID = 'Odoo'
        self.Odoocredentials = ['user', 'password', 'url', 'db']
        self.event = {'venueid': '1', 'typeid': '1'}
        self.context = None  # for now

    def testMatchesCorrectPOSAPI(self) -> None:
        self.assertEqual(self.handler.getPOSObject('Odoo', '1', self.Odoocredentials).POStype, self.OdooposID)

    def testRaisesErrorWithUnknownPOSID(self) -> None:
        self.assertRaises(NotImplementedError, self.handler.getPOSObject, 'UnknownAPI', '1', self.Odoocredentials)

    def testHandlesRequestWithMockDB(self) -> None:
        self.handler.handle_request(self.event, self.context)
        self.mockDB.getTable.assert_called_once()


class SubscriptMock(Mock):  # need a subscriptable mock, need to think about how to not set posid to Odoo only
    def __getitem__(self, item) -> dict:
        return {'posid': 'Odoo', 'poscreds': ['user', 'password', 'url', 'db']}
