from unittest import TestCase
from unittest.mock import Mock, patch

from main.lambdautils.ConfirmationEmail import ConfirmationEmail


class TestConfirmationEmail(TestCase):
    def setUp(self) -> None:
        self.testCustomerEmailAddress = 'abc@abc.abc'
        self.testOrder = '{\n  "data": {\n    "object": {\n      "id": ' \
                         '"cs_test_O4bwiLSgP7uC0EzGBtk1i28kvVTZdG782if9IWwzQc6pblOWuIEnj2DR",' \
                         '\n      "object": "checkout.session",\n      "billing_address_collection": null,' \
                         '"display_items": [\n        {\n          ' \
                         '"amount": 100,\n          "currency": "gbp",\n          "custom": {\n            ' \
                         '"description": null,\n            "images": null,\n            "name": "Coke"\n     ' \
                         '     },\n          "quantity": 2,\n          "type": "custom"\n        },' \
                         '\n        {\n          "amount": 1500,\n          "currency": "gbp",\n          ' \
                         '"custom": {\n            "description": null,\n            "images": null,' \
                         '\n            "name": "Bolognese"\n          },\n          "quantity": 2,' \
                         '\n          "type": "custom"\n        }\n      ],\n      "livemode": false,' \
                         '\n      "locale": null,\n      "metadata": {\n        "venue": "Library Cafe",' \
                         '\n        "venueid": "2",\n        "typeid": "1"}}}}'
        self.emailer = ConfirmationEmail(self.testOrder, self.testCustomerEmailAddress)

    @patch('main.lambdautils.ConfirmationEmail.smtplib.SMTP')
    @patch('main.lambdautils.ConfirmationEmail.MIMEMultipart')
    def testAttemptsToSendEmail(self, mockSMTP, mockMIME):
        self.emailer.sendConfirmation()
        self.assertTrue(mockSMTP.called)

    def testCalculatesTotalCorrectly(self):
        self.emailer.order = {
            'data': {'object': {'display_items': [{'amount': 250, 'quantity': 12}, {'amount': 400, 'quantity': 5}]}}}
        expected = 50
        self.assertEqual(expected, self.emailer.calculateTotal())
