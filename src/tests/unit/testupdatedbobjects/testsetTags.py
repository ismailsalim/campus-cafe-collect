from unittest import TestCase
from unittest.mock import Mock
from main.updatedbobjects.setTags import SetTagsHandler


class TestSetTagsHandler(TestCase):
    def setUp(self) -> None:
        self.mockDB = Mock()
        self.handler = SetTagsHandler(self.mockDB)
