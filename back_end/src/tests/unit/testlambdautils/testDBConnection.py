from unittest import TestCase
from unittest.mock import patch
from main.lambdautils.DBConnection import DynamoConn


class TestDynamoConn(TestCase):
    def setUp(self) -> None:
        self.tableName = 'testTable'
        self.conn = DynamoConn(self.tableName)

    def testUpdatesTable(self):
        newTable = 'newTable'
        self.assertNotEqual(newTable, self.conn.table)
        self.conn.updateTable(newTable)
        self.assertEqual(newTable, self.conn.table)

    @patch('boto3.resource')
    def testReturnsTable(self, mockResource):
        table = mockResource().Table()
        self.assertEqual(table, self.conn.getTable())

    def testAcceptsAttribute(self):
        self.assertEqual(self.tableName, self.conn.table)