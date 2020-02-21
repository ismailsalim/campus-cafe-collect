from unittest import TestCase
from unittest.mock import Mock, patch
from main.updatedbobjects.setTags import SetTagsHandler
from main.lambdautils.DBConnection import DynamoConn
import json


class TestSetTagsHandler(TestCase):
    def setUp(self) -> None:
        self.mockDB = Mock(spec=DynamoConn)
        self.handler = SetTagsHandler(self.mockDB)
        self.venueTypeID = '1'
        self.typeID = '1'
        self.venue = 'testvenue'
        self.unprocessedtags = ['abc11', 'abc1-1', '---', '3242343', 'test', 'test1', 'anotherTest', 'noDigits', '12',
                                'test!with!punctuation/.,/.', 'a', '']
        self.tagsWithDigitsRemoved = ['---', 'test', 'anotherTest', 'noDigits', 'test!with!punctuation/.,/.', 'a', '']
        self.tagsWithPunctuationFormatting = ['abc', 'abc-', '---', '', 'test', 'test', 'anotherTest',
                                              'noDigits', '', 'testwithpunctuation', 'a', '']
        self.lengthFilteredTags = ['abc11', 'abc1-1', '---', '3242343', 'test', 'test1', 'anotherTest', 'noDigits',
                                   '12', 'test!with!punctuation/.,/.']
        self.processedtags = ['---', 'test', 'anotherTest', 'noDigits', 'testwithpunctuation']
        self.menu = {
            'c1': [('a1', 'p1')],
            'c2': [('a2', 'p2')],
            'c3': [('a3', 'p3')]
        }
        self.menuTagsList = {'a1', 'a2', 'a3'}
        self.venueTags = {
            '---': [[self.venue, self.typeID]],
            'test': [[self.venue, self.typeID]],
            'anotherTest': [[self.venue, self.typeID]],
            'noDigits': [[self.venue, self.typeID]],
            'testwithpunctuation': [[self.venue, self.typeID]],
        }
        self.tagCounts = {'---': 1, 'test': 1, 'anotherTest': 1, 'noDigits': 1, 'testwithpunctuation': 1}

    MOCKGETVENUESRESULT = {'statusCode': 200,
                           'body': json.dumps([{'venueid': '1', 'typeid': '1'}, {'venueid': '2', 'typeid': '2'}])}

    MOCKGETMENURESULT = {'statusCode': 200,
                         'body': json.dumps({
                             'categ1': [('itemOne', 'priceOne')],
                             'categ2': [('itemTwo', 'priceTwo')],
                             'categ3': [('itemThree', 'priceThree')]
                         })}

    def testRemovesTagsWithDigits(self):
        self.assertEqual(self.handler.removeTagsWithDigits(self.unprocessedtags), self.tagsWithDigitsRemoved)

    def testRemovesPunctuationInTags(self):
        self.assertEqual(self.handler.removePunctuationInTags(self.unprocessedtags), self.tagsWithPunctuationFormatting)

    def testFiltersTagsByLength(self):
        self.assertEqual(self.handler.filterTagLength(self.unprocessedtags), self.lengthFilteredTags)

    def testProcessesTagsCorrectly(self):
        self.assertEqual(self.handler.process_tags(self.unprocessedtags), self.processedtags)

    def testGetsTagsFromTheMenu(self):
        self.assertEqual(self.handler.getTagsFromMenu(self.menu), self.menuTagsList)

    def testGetTagCounts(self):
        self.assertEqual(self.handler.add_to_tags_counts(self.processedtags, {}), self.tagCounts)

    def testAddsToTagsVenues(self):
        self.assertEqual(self.handler.add_to_tags_venues(self.processedtags, self.venue, self.typeID, {}),
                         self.venueTags)

    def testUpdatesTable(self):
        newTable = 'DifferentName'
        self.handler.updateTable(newTable)
        self.handler.db.updateTable.assert_called_once()

    @patch('main.lambdautils.DBConnection.DynamoConn')
    @patch('main.updatedbobjects.setTags.SetTagsHandler.getAllVenues', return_value=MOCKGETVENUESRESULT)
    @patch('main.updatedbobjects.setTags.SetTagsHandler.getMenuForVenue', return_value=MOCKGETMENURESULT)
    def testProcessesEvent(self, mockDB, mockGetVenueMethod, mockGetMenuMethod):
        self.assertEqual(self.handler.handle_request(None, None), {'statusCode': self.handler.successCode})
