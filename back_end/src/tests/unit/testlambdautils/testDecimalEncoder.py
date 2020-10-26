from unittest import TestCase
from main.lambdautils.DecimalEncoder import DecimalEncoder
import decimal


class TestDecimalEncoder(TestCase):
    def setUp(self) -> None:
        self.encoder = DecimalEncoder()
        self.decimalValue = decimal.Decimal(10)

    def testReturnsFloatsOfDecimalTypes(self):
        self.assertEqual(self.encoder.default(self.decimalValue), float(self.decimalValue))
