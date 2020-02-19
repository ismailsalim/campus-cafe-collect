from unittest import TestCase
from unittest.mock import Mock
from main.updatedbobjects.setPriceRank import SetPriceRankHandler


class TestSetPriceRank(TestCase):
    def setUp(self) -> None:
        self.mockDB = Mock()
        self.handler = SetPriceRankHandler(Mock)
        self.genericPriceList = [12, 16, 19, 20, 15.4, 0.99, 100]
        self.genericPriceListRank = 3
        self.menu = {
            'first': [('a', '1'), ('a', '1'), ('a', '1')],
            'second': [('b', '2'), ('b', '2'), ('b', '2')],
            'third': [('c', '3'), ('c', '3'), ('c', '3')]
        }
        self.priceListFromMenu = [1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0]

    def testRanksPriceListCorrectly(self):
        self.assertEqual(self.genericPriceListRank, self.handler.rankPriceList(self.genericPriceList))

    def testConvertsToFloat(self):
        self.assertEqual(self.priceListFromMenu, self.handler.getPriceList(self.menu))
