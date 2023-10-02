from unittest import TestCase

import textarium.extraction as extraction

class TestExtraction(TestCase):
    def test_extract_words_en_0(self):
        test_input = "This line has 5 tokens"
        expected_result = ["This", "line", "has", "5", "tokens"]
        result = extraction.extract_words(test_input)
        self.assertListEqual(expected_result, result)

    def test_extract_words_ru_0(self):
        test_input = "В этой строке 5 токенов"
        expected_result = ["В", "этой", "строке", "5", "токенов"]
        result = extraction.extract_words(test_input)
        self.assertListEqual(expected_result, result)

    def test_extract_sentences_en_0(self):
        text_input = """
        Hello! My name is Robbie. 
        Please, write an email to Mr. Parker. 
        His email: parker@gmail.com.
        """
        expected_result = [
            "Hello!", "My name is Robbie.", 
            "Please, write an email to Mr. Parker.", 
            "His email: parker@gmail.com."
        ]
        result = extraction.extract_sentences(text_input, lang='en')
        self.assertListEqual(expected_result, result)

    def test_extract_sentences_ru_0(self):
        text_input = """
        Привет! Меня зовут Робби.
        Пожалуйста, напиши письмо (т. е. e-mail) Паркеру.
        Его адрес: parker@gmail.com.
        """
        expected_result = [
            "Привет!", "Меня зовут Робби.",
            "Пожалуйста, напиши письмо (т. е. e-mail) Паркеру.",
            "Его адрес: parker@gmail.com."
        ]
        result = extraction.extract_sentences(text_input, lang='ru')
        self.assertListEqual(expected_result, result)

    def test_extract_urls_0(self):
        text_input = """
        There is one link: http://google.com.
        And another one: https://www.google.com/images?v=1&p=2!
        This is not a link: test@gmail.com
        """
        exptected_result = [
            "http://google.com",
            "https://www.google.com/images?v=1&p=2"
        ]
        result = extraction.extract_urls(text_input)
        self.assertListEqual(exptected_result, result)

    def test_extract_emails(self):
        text_input = """
        Please write to stan.dobryakov@gmail.com
        and add to cc another email of @sdobryakov: std@gmail.com
        """
        expected_result = [
            "stan.dobryakov@gmail.com",
            "std@gmail.com"
        ]
        result = extraction.extract_emails(text_input)
        self.assertListEqual(expected_result, result)

    def test_extract_dates(self):
        text_input = """
        The cerememony will take place on 21-02-2013
        despite of the fact that I was born on 15/04/1993
        """
        expected_result = ["2013-02-21T00:00:00", "1993-04-15T00:00:00"]
        result = [d.isoformat() for d in extraction.extract_dates(text_input)]
        self.assertListEqual(expected_result, result)

    def test_extract_ngrams(self):
        text_input = """
        this sentence consists of 8 bigrams and 7 trigrams
        """
        expected_result = [
            ("this", "sentence"),
            ("sentence", "consists"),
            ("consists", "of"),
            ("of", "8"),
            ("8", "bigrams"),
            ("bigrams", "and"),
            ("and", "7"),
            ("7", "trigrams")
        ]
        result = extraction.extract_ngrams(text_input, n=2)
        self.assertListEqual(expected_result, result)
