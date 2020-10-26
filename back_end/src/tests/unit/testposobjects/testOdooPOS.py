from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock

from main.posobjects.OdooPOS import OdooPOS


class TestOdooPos(TestCase):
    def setUp(self) -> None:
        self.venueID = '1'
        self.credentials = ['user', 'password', 'url', 'db']
        self.POSinstance = OdooPOS(self.venueID, self.credentials)
        self.POSinstance.conn = MagicMock()
        self.POSinstance.conn.execute_kw = MagicMock(return_value=[{'id': '##'}])
        self.unformattedMenu = [
            {'display_name': 'a1', 'list_price': 'p1', 'categ_id': (1, 'c1'), 'taxes_id': 't'},
            {'display_name': 'a2', 'list_price': 'p2', 'categ_id': (2, 'c2'), 'taxes_id': 't'},
            {'display_name': 'a3', 'list_price': 'p3', 'categ_id': (3, 'c3'), 'taxes_id': 't'}
        ]
        self.formattedMenu = {
            'c1': [('a1', 'p1')],
            'c2': [('a2', 'p2')],
            'c3': [('a3', 'p3')]
        }

        self.orderTestCase = {'customerEmail': 'abc@abc.abc',
                              'data': {'object': {
                                  'display_items': [{'amount': 1, 'quantity': 1, 'custom': {'name': 'AAA'}}],
                                  'id': 'ABCD1234'}}}
        self.processOrder = [{'price_subtotal': 10, 'price_subtotal_incl': 12},
                             {'price_subtotal': 99, 'price_subtotal_incl': 104.32},
                             {'price_subtotal': 52, 'price_subtotal_incl': 60.5},
                             {'price_subtotal': 20, 'price_subtotal_incl': 32}]

    def testAssignsCredentialsCorrectly(self):
        self.assertEqual(self.POSinstance.username, self.credentials[0])
        self.assertEqual(self.POSinstance.password, self.credentials[1])
        self.assertEqual(self.POSinstance.url, self.credentials[2])
        self.assertEqual(self.POSinstance.db, self.credentials[3])

    def testFormatsMenuCorrectly(self):
        self.assertEqual(self.formattedMenu, self.POSinstance.formatMenu(self.unformattedMenu))

    def testRaisesRuntimeErrorWhenMenuIsEmpty(self):
        with self.assertRaises(RuntimeError):
            self.POSinstance.formatMenu([])

    @patch('main.posobjects.OdooPOS.OdooPOS.getConnection')
    def testPushesOrderCorrectly(self, mockConnectionMethod):
        self.POSinstance.session_id = '##'
        expected = 'ABCD1234'
        self.assertEqual(expected, self.POSinstance.pushOrder(self.orderTestCase))

    @patch('main.posobjects.OdooPOS.OdooPOS.executeToOdoo', return_value=['1'])
    def testReturnsCorrectClientIDIfClientExists(self, mockedFunction):
        dummyEmail = 'existing@email.com'
        expected = '1'
        self.assertEqual(self.POSinstance.deriveClientID(dummyEmail), expected)

    @patch('main.posobjects.OdooPOS.OdooPOS.executeToOdoo', side_effect=[[], '1'])
    def testReturnsNewClientIDIfClientDoesNotExist(self, mockedFunction):
        # side_effect parameter is iterable, therefore we can mimic the case
        # where executeToOdoo() does not find a client and then returns the
        # ID of the newly created client when called again
        dummyEmail = 'existing@email.com'
        expected = '1'
        self.assertEqual(self.POSinstance.deriveClientID(dummyEmail), expected)

    def testCalculatesCorrectTotalsFromList(self):
        expectedSubTotalWithTax = 208.82
        expectedAmountTax = 27.82
        actualSubTotalWithTax, actualAmountTax = self.POSinstance.calculateTotals(self.processOrder)
        self.assertAlmostEqual(actualSubTotalWithTax, expectedSubTotalWithTax)
        self.assertAlmostEqual(actualAmountTax, expectedAmountTax)
