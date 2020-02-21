import unittest
from unittest import TestCase

from main.posobjects.OdooPOS import OdooPOS


class TestOdooPos(TestCase):
    def setUp(self) -> None:
        self.venueID = '1'
        self.credentials = ['user', 'password', 'url', 'db']
        self.api_instance = OdooPOS(self.venueID,self.credentials)
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

    def testAssignsCredentialsCorrectly(self):
        self.assertEqual(self.api_instance.username, self.credentials[0])
        self.assertEqual(self.api_instance.password, self.credentials[1])
        self.assertEqual(self.api_instance.url, self.credentials[2])
        self.assertEqual(self.api_instance.db, self.credentials[3])

    def testFormatsMenuCorrectly(self):
        self.assertEqual(self.formattedMenu, self.api_instance.formatMenu(self.unformattedMenu))

    def testRaisesRuntimeErrorWhenMenuIsEmpty(self):
        with self.assertRaises(RuntimeError):
            self.api_instance.formatMenu([])
