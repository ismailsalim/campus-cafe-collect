import abc
from DecimalEncoder import DecimalEncoder
from DBConnection import DynamoConn


class BaseLambdaHandler(metaclass=abc.ABCMeta):
    def __init__(self, dbObject: DynamoConn):
        self.db = dbObject
        self.clientErrorCode = 404
        self.successCode = 200
        self.encoder = DecimalEncoder

    @abc.abstractmethod
    def handle_request(self, event, context):
        pass
