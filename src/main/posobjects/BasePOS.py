import abc


class BasePOS(metaclass=abc.ABCMeta):
    def __init__(self, venueID: str):
        self.venueID = venueID

    @abc.abstractmethod
    def getMenu(self):
        pass
