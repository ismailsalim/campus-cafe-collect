from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
from main.menuobjects.getMenu import GetMenuHandler
from main.lambdautils.DBConnection import DynamoConn
import abc


class UpdateHandler(BaseLambdaHandler, metaclass=abc.ABCMeta):
    """
    updates are currently made to all venues, hence for either update type
    we require methods to fetch all venues and menu for those venues
    This abstract class implements those methods which other handlers will inherit from
    """

    def __init__(self, dbObject):
        super().__init__(dbObject)

    @staticmethod
    def getMenuForVenue(params: dict) -> dict:
        getMenuHandler = GetMenuHandler(DynamoConn('Credentials'))
        return getMenuHandler.handle_request(event=params, context={})

    @staticmethod
    def getAllVenues() -> list:
        allVenues = []
        try:
            table = DynamoConn("Venues").getTable()
            response = table.scan()
            allVenues += [venue for venue in response['Items']]
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                allVenues += [venue for venue in response['Items']]
            return allVenues
        except Exception as e:
            print(e)
            return []
