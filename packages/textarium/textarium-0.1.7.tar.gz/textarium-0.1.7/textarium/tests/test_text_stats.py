from unittest import TestCase

from textarium.stats import text_stats as ts

class TestTextStats(TestCase):
    def test_characters_count(self):
        input = "This text contains 33 characters."
        expected_result = 33
        self.assertEqual(ts.characters_count(input), expected_result)

    def test_words_count(self):
        input = "This text contains 5 words."
        expected_result = 5
        self.assertEqual(ts.words_count(input), expected_result)

    def test_senteces_count(self):
        input = "Hi! I'm Jack. How are you doing?"
        expected_result = 3
        self.assertEqual(ts.sentences_count(input), expected_result)

    def test_urls_count(self):
        input = "What is better: http://google.com or https://www.yahoo.com?"
        expected_result = 2
        self.assertEqual(ts.urls_count(input), expected_result)

    def test_unique_words_count(self):
        input = "Hi! I am Jack. How are you doing? How was your day? Jack, what are your plans?"
        expected_result = 13
        self.assertEqual(ts.unique_words_count(input), expected_result)

    def test_characters_per_word(self):
        input = "This text contains 33 characters."
        expected_result = (4 + 4 + 8 + 10) / 4
        self.assertEqual(ts.characters_per_word(input), expected_result)

    def test_words_per_sentence(self):
        input = "Hi! I am Jack. How are you doing? How was your day? Jack, what are your plans?"
        expected_result = (1 + 3 + 4 + 4 + 5) / 5
        self.assertEqual(ts.words_per_sentence(input), expected_result)

    def test_count_words_by_predicat(self):
        input = "Hi! I am Jack. How are you doing? How was your day? Jack, what are your plans?"
        predicat_func = lambda x: len(x) <= 2
        expected_result = 3
        self.assertEqual(ts.count_words_by_predicat(input, predicat_func), expected_result)

    def test_long_words_count(self):
        input = "This sentence contains 2 long words"
        expected_result = 2
        self.assertEqual(ts.long_words_count(input), expected_result)

    def test_short_words_count(self):
        input = "This sentence contains 5 short words: i, am, one, two."
        expected_result = 5
        self.assertEqual(ts.short_words_count(input), expected_result)