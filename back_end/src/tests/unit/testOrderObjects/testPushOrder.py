from unittest import TestCase
from unittest.mock import Mock, patch

from main.orderobjects.pushOrder import PushOrderHandler
import json


class DummyClass(object):
    # object to be returned byt the patched stripe module calls
    # only contains a type attribute set depending on the initialisation value
    def __init__(self, TYPE: int):
        self.type = 'checkout.session.completed' if TYPE else 'failType'


class TestPushOrderHandler(TestCase):
    def setUp(self) -> None:
        self.mockDB = SubscriptMock()
        self.handler = PushOrderHandler(self.mockDB)
        self.testEvent = {'body': '{\n  "id": "evt_1GYcvpHUyJoJD8SkEzvyBaZ7",\n  "object": "event",\n  "account": '
                                  '"acct_1GSkQzHUyJoJD8Sk",\n  "api_version": "2020-03-02",\n  "created": 1587063565,'
                                  '\n  "data": {\n    "object": {\n      "id": '
                                  '"cs_test_O4bwiLSgP7uC0EzGBtk1i28kvVTZdG782if9IWwzQc6pblOWuIEnj2DR",'
                                  '\n      "object": "checkout.session",\n      "billing_address_collection": null,'
                                  '\n      "cancel_url": "https://test.dolxjcfav4ei2.amplifyapp.com/venues/2/1",'
                                  '\n      "client_reference_id": null,\n      "customer": "cus_H6qd2LOQbZmUsK",'
                                  '\n      "customer_email": null,\n      "display_items": [\n        {\n          '
                                  '"amount": 100,\n          "currency": "gbp",\n          "custom": {\n            '
                                  '"description": null,\n            "images": null,\n            "name": "Coke"\n     '
                                  '     },\n          "quantity": 2,\n          "type": "custom"\n        },'
                                  '\n        {\n          "amount": 1500,\n          "currency": "gbp",\n          '
                                  '"custom": {\n            "description": null,\n            "images": null,'
                                  '\n            "name": "Bolognese"\n          },\n          "quantity": 2,'
                                  '\n          "type": "custom"\n        }\n      ],\n      "livemode": false,'
                                  '\n      "locale": null,\n      "metadata": {\n        "venue": "Library Cafe",'
                                  '\n        "venueid": "2",\n        "typeid": "1",\n        "acct": '
                                  '"acct_1GSkQzHUyJoJD8Sk"\n      },\n      "mode": "payment",'
                                  '\n      "payment_intent": "pi_1GYcujHUyJoJD8SkMqilV6tl",'
                                  '\n      "payment_method_types": [\n        "card"\n      ],\n      "setup_intent": '
                                  'null,\n      "shipping": null,\n      "shipping_address_collection": null,'
                                  '\n      "submit_type": null,\n      "subscription": null,\n      "success_url": '
                                  '"https://test.dolxjcfav4ei2.amplifyapp.com/success?session_id={'
                                  'CHECKOUT_SESSION_ID}\\u0026acct=acct_1GSkQzHUyJoJD8Sk"\n    }\n  },\n  "livemode": '
                                  'false,\n  "pending_webhooks": 1,\n  "request": {\n    "id": null,'
                                  '\n    "idempotency_key": null\n  },\n  "type": "checkout.session.completed"\n}',
                          'isBase64Encoded': False}

    @patch('main.orderobjects.pushOrder.PushOrderHandler.checkPaymentWasMade', return_value=False)
    def testReturnsErrorCodeIfPaymentNotMade(self, mockCheckMethod):
        expected = {'statusCode': self.handler.clientErrorCode}
        self.assertEqual(expected, self.handler.handle_request(self.testEvent, {}))

    @patch('main.orderobjects.pushOrder.PushOrderHandler.getCustomerEmail', return_value='abc@abc.abc')
    @patch('main.orderobjects.pushOrder.PushOrderHandler.checkPaymentWasMade', return_value=True)
    @patch('main.orderobjects.pushOrder.OdooPOS.pushOrder', return_value='###')
    def testProcessNormalOrder(self, mockedPOSAPIMethod, mockedCheckMethod, mockHandlerMethod):
        expected = {'statusCode': self.handler.successCode,
                    'body': json.dumps('###')}
        self.assertEqual(expected, self.handler.handle_request(self.testEvent, {}))

    @patch('main.orderobjects.pushOrder.stripe.Customer.retrieve', return_value={'email': 'abc@abc.abc'})
    def testGetsCorrectCustomerData(self, mockedStripe):
        event = json.loads(self.testEvent['body'].replace("'", "\'"))
        expected = 'abc@abc.abc'
        self.assertEqual(expected, self.handler.getCustomerEmail(event))

    @patch('main.orderobjects.pushOrder.stripe.Event.construct_from', return_value=DummyClass(1))
    def testReturnsTrueIfPaymentWasMade(self, mockedStripeMethod):
        event = json.loads(self.testEvent['body'].replace("'", "\'"))
        self.assertTrue(self.handler.checkPaymentWasMade(event))

    @patch('main.orderobjects.pushOrder.stripe.Event.construct_from', side_effect=ValueError)
    def testReturnsFalseIfValueError(self, mockedStripeMethod):
        event = json.loads(self.testEvent['body'].replace("'", "\'"))
        self.assertFalse(self.handler.checkPaymentWasMade(event))

    @patch('main.orderobjects.pushOrder.stripe.Event.construct_from', return_value=DummyClass(0))
    def testReturnsFalseIfPaymentWasNotMade(self, mockedStripeMethod):
        event = json.loads(self.testEvent['body'].replace("'", "\'"))
        self.assertFalse(self.handler.checkPaymentWasMade(event))

    def testReturnsCorrectPOSObject(self):
        venueID = '#'
        creds = ['#', '#', '#', '#']
        posID = 'Odoo'
        expected = 'Odoo'
        self.assertEqual(expected, self.handler.getPOSObject(posID, venueID, creds).POStype)

    def testRaisesErrorIfUnknowPOSIdPassed(self):
        venueID = '#'
        creds = ['#', '#', '#', '#']
        posID = 'UNKOWN'
        with self.assertRaises(NotImplementedError):
            self.handler.getPOSObject(posID, venueID, creds)


class SubscriptMock(Mock):  # need a subscriptable mock, need to think about how to not set posid to Odoo only
    def __getitem__(self, item):
        returnDicts = {'Item': {'posid': 'Odoo', 'poscreds': ['#', '#', '#', '#']}}
        return returnDicts[item]
