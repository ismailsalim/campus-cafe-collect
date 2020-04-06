import boto3

class DynamoConn:
    def __init__(self, table: str) -> None:
        self.table = table

    def getTable(self):
        db = boto3.resource('dynamodb', region_name='eu-west-2')
        return db.Table(self.table)

    def updateTable(self, newTable):
        self.table = newTable
