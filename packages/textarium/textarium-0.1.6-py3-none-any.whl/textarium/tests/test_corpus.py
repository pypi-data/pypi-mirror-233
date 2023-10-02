from unittest import TestCase
from textarium.corpus import Corpus

class TestText(TestCase):
    def test_prepare_en_0(self):
        input = [
            "Hello! My name is Mr.Parker.",
            "I have a website https://parker.com.",
            "It has about 5000 visitors per day.",
            "I track it with a simple html-block like this:",
            "<div>Google.Analytics</div>",
        ]
        expected_result = [
            "hello my name is mr parker",
            "i have a website",
            "it ha about visitor per day",
            "i track it with a simple html block like this",
            "google analytics",
        ]
        corpus = Corpus(input, lang='en')
        corpus.prepare()
        self.assertListEqual(expected_result, [t.prepared_text for t in corpus.corpus])

    def test_filter_raw(self):
        input = [
            "Hello! My name is Mr.Parker.",
            "I have a website https://parker.com.",
            "It has about 5000 visitors per day.",
            "I track it with a simple html-block like this:",
            "<div>Google.Analytics</div>",
        ]
        condition = lambda x : len(x.split()) > 5
        expected_result = [
            "It has about 5000 visitors per day.",
            "I track it with a simple html-block like this:",
        ]
        corpus = Corpus(input, lang='en')
        corpus.filter(condition=condition)
        self.assertListEqual(expected_result, [t.raw_text for t in corpus.corpus])
