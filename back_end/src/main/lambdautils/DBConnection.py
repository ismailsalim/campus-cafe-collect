import boto3
from main.lambdautils.BaseConn import BaseConn


class DynamoConn(BaseConn):
    """
    Connection object encapsulating the link to the DynamoDB database
    """
    def __init__(self, table: str) -> None:
        super().__init__()
        self.table = table

    def getTable(self):
        db = boto3.resource('dynamodb', region_name='eu-west-2')
        return db.Table(self.table)

    def updateTable(self, newTable) -> None:
        self.table = newTable
