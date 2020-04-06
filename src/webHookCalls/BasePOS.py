import abc


class BasePOS(metaclass=abc.ABCMeta):
    def __init__(self, venueID: str):
        self.venueID = venueID
        self.vat = 1.2
    @abc.abstractmethod
    def getMenu(self):
        pass

    @abc.abstractmethod
    def pushOrder(self, order):
        pass
