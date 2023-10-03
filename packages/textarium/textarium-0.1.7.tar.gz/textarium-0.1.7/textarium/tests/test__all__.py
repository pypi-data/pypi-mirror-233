from unittest import TestCase
import collections
import textarium

class TestCollections(TestCase):
    def test_no_duplicates_in_textarium__all__(self):
        dups = {k: v for k, v in collections.Counter(textarium.__all__).items() if v > 1}
        self.assertTrue(len(dups) == 0)