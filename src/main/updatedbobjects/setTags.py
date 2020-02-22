from main.lambdautils.BaseLambdaHandler import BaseLambdaHandler
from main.lambdautils.DBConnection import DynamoConn
from main.venueobjects.getVenues import GetVenuesHandler
from main.menuobjects.getMenu import GetMenuHandler
import json


# default dbOject table should be venues
class SetTagsHandler(BaseLambdaHandler):
    def __init__(self, dbObject):
        super().__init__(dbObject)

    def handle_request(self, event, context):
        dbTable = self.db.getTable()

        # fetch all the venue data
        response = self.getAllVenues()
        if response['statusCode'] == self.successCode:
            venues = json.loads(response['body'])
            # do something here if fails
        else:
            return {
                'statusCode': self.clientErrorCode,
            }

        tags_and_counts = {}
        tags_and_venues = {}

        for venue in venues:
            venue_id = venue['venueid']
            type_id = venue['typeid']

            # fetching the menu from a specific venue
            input_params = {
                "venueid": venue_id,
                "typeid": type_id
            }

            print("CALLING GET MENU")
            response = self.getMenuForVenue(input_params)

            if response['statusCode'] != self.successCode:
                continue

            menu = json.loads(response['body'])

            venue_tags = self.getTagsFromMenu(menu)

            venue_tags = self.process_tags(list(venue_tags))

            self.add_to_tags_counts(venue_tags, tags_and_counts)

            self.add_to_tags_venues(venue_tags, venue_id, type_id, tags_and_venues)

            print("\nVENUE TAG SET", venue_tags, "\n")
            # updating tags attribute for each venue in venues
            dbTable.update_item(  # TODO not the best implementation here. look to refactor later
                Key={
                    'venueid': venue_id,
                    'typeid': type_id
                },
                UpdateExpression="set tags = :t",
                ExpressionAttributeValues={
                    ':t': venue_tags
                }
            )

        self.updateTable('FoodTags')
        dbTable = self.db.getTable()
        # NOTE: Each list item in venues will be a list [venue_id, type]
        for (t1, count), (t2, venues) in zip(tags_and_counts.items(), tags_and_venues.items()):
            dbTable.put_item(
                TableName='FoodTags',
                Item={
                    'foodtag': t1,
                    'count': count,
                    'venues': venues
                }
            )

        print("\nFINAL TAG and COUNTS", tags_and_counts)
        print("FINAL TAG and VENUES", tags_and_venues, "\n")

        return {
            'statusCode': self.successCode,
        }

    def process_tags(self, tags_list):
        tags_list = self.removeTagsWithDigits(tags_list)
        tags_list = self.removePunctuationInTags(tags_list)
        tags_list = self.filterTagLength(tags_list)

        return tags_list

    def updateTable(self, newTable):
        self.db.updateTable(newTable)

    @staticmethod
    def getAllVenues():
        conn = DynamoConn("Venues")  # will be used later on as well
        getVenuesHandler = GetVenuesHandler(conn)
        return getVenuesHandler.handle_request(event=None, context=None)

    @staticmethod
    def getMenuForVenue(params):
        getMenuHandler = GetMenuHandler(DynamoConn('Credentials'))
        return getMenuHandler.handle_request(event=params, context=None)

    @staticmethod
    def removeTagsWithDigits(tags_list):
        # removes tags with digits
        return [x for x in tags_list if not any(x1.isdigit() for x1 in x)]

    @staticmethod
    def removePunctuationInTags(tags_list):
        # removes punctuation from tags
        return [''.join(letter for letter in tag if letter == '-' or letter.isalpha()) for tag in tags_list]

    @staticmethod
    def filterTagLength(tags_list):
        # remove tags of length less than two
        return [tag for tag in tags_list if len(tag) >= 2]

    @staticmethod
    def add_to_tags_counts(tags, tags_and_counts):
        for tag in tags:
            if tag not in tags_and_counts:
                tags_and_counts[tag] = 1
            else:
                tags_and_counts[tag] += 1
        return tags_and_counts

    @staticmethod
    def add_to_tags_venues(tags, venue, type_id, tags_and_venues):
        for tag in tags:
            if tag not in tags_and_venues:
                tags_and_venues[tag] = [[venue, type_id]]
            else:
                tags_and_venues[tag].append([venue, type_id])
        return tags_and_venues

    @staticmethod
    def getTagsFromMenu(menu):
        # generate tags associated with each venue
        name_idx = 1
        venue_tags = set()
        for category in menu:
            items = menu[category]
            for item in items:
                tags = item[name_idx].lower().split()
                venue_tags.update(tags)
        return venue_tags
