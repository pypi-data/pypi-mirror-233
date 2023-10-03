from unittest import TestCase
from textarium.corpus import Corpus

test_texts_list = [
    "Hello! My name is Mr.Parker.",
    "I have a website https://parker.com.",
    "It has about 5000 visitors per day.",
    "I track it with a simple html-block like this:",
    "<div>Google.Analytics</div>",
]

class TestCorpus(TestCase):
    def test_prepare_en_0(self):
        expected_result = [
            "hello my name is mr parker",
            "i have a website",
            "it ha about visitor per day",
            "i track it with a simple html block like this",
            "google analytics",
        ]
        corpus = Corpus(test_texts_list, lang='en')
        corpus.prepare()
        self.assertListEqual(expected_result, [t.prepared_text for t in corpus.corpus])

    def test_filter_raw_attr_inplace_false(self):
        condition = lambda x : len(x.split()) > 5
        expected_result = [
            "It has about 5000 visitors per day.",
            "I track it with a simple html-block like this:",
        ]
        corpus = Corpus(test_texts_list, lang='en')
        result = corpus.filter(condition=condition, attribute="raw_text")
        self.assertListEqual(expected_result, [t.raw_text for t in result.corpus])

    def test_filter_raw_attr_inplace_true(self):
        condition = lambda x : len(x.split()) > 5
        expected_result = [
            "It has about 5000 visitors per day.",
            "I track it with a simple html-block like this:",
        ]
        corpus = Corpus(test_texts_list, lang='en')
        corpus.filter(condition=condition, attribute="raw_text", inplace=True)
        self.assertListEqual(expected_result, [t.raw_text for t in corpus.corpus])

    def test_filter_prepared_attr_inplace_false(self):
        condition = lambda x : "visitor" in x
        expected_result = [
            "it ha about visitor per day",
        ]
        corpus = Corpus(test_texts_list, lang='en')
        corpus.prepare()
        result = corpus.filter(condition=condition, attribute="prepared_text")
        self.assertListEqual(expected_result, [t.prepared_text for t in result.corpus])

    def test_get_item(self):
        corpus = Corpus(test_texts_list, lang='en')
        idx = 2
        expected_result = test_texts_list[2]
        result = corpus[idx].raw_text
        self.assertEqual(expected_result, result)

    def test_len(self):
        corpus = Corpus(test_texts_list, lang='en')
        expected_result = len(test_texts_list)
        result = len(corpus)
        self.assertEqual(expected_result, result)

    def test_info(self):
        corpus = Corpus(test_texts_list, lang='en')
        corpus.info()

