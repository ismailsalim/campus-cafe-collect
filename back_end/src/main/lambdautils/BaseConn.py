import abc


class BaseConn(metaclass=abc.ABCMeta):
    """
    base abstract class to encapsulate connetions to different databases
    """

    @abc.abstractmethod
    def getTable(self):
        pass

    @abc.abstractmethod
    def updateTable(self, table: str):
        pass
