from unittest import TestCase
from textarium.collections import get_stopwords

class TestCollections(TestCase):
    def test_get_stopwords_en_0(self):
        sw = get_stopwords()
        self.assertTrue(len(sw) > 0)
        self.assertTrue(type(sw) == list)

    def test_get_stopwords_ru_0(self):
        sw = get_stopwords(lang='ru')
        self.assertTrue(len(sw) > 0)
        self.assertTrue(type(sw) == list)