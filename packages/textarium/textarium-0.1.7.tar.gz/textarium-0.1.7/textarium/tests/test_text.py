from unittest import TestCase

from textarium.text import Text

class TestText(TestCase):
    def test_prepare_en_0(self):
        input_text = """
        Hello! My name is Mr.Parker.
        I have a website https://parker.com.
        It has about 5000 visitors per day.
        I track it with a simple html-block like this:
        <div>Google.Analytics</div>
        """
        expected_result = (
            "hello my name is mr parker"\
            " i have a website it ha about visitor per day"\
            " i track it with a simple html block like this"\
            " google analytics"
        )
        text = Text(input_text, lang='en')
        text.prepare()
        self.assertEqual(expected_result, text.prepared_text)

    def test_prepare_ru_0(self):
        input_text = """
        Добрый день! Мое имя мистер Паркер.
        У меня есть веб-сайт https://parker.com.
        Трекер насчитывает 5000 посетителей в день.
        Я слежу за этим с помощью простого html-блока:
        <div>Google.Analytics</div>
        """
        expected_result = (
            "добрый день мой имя мистер паркер"\
            " у я есть веб сайт трекер насчитывать посетитель в день"\
            " я следить за это с помощь простой html блок"\
            " google analytics"
        )
        text = Text(input_text, lang='ru')
        text.prepare()
        self.assertEqual(expected_result, text.prepared_text)