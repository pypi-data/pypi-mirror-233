# -*- coding: utf-8 -*-

"""
Text class.
"""

from typing import List
from textarium.utils import pipeline
import textarium.preprocessing as tp

class Text:
    def __init__(self, text: str, lang: str = 'en'):
        self.lang = lang
        self.raw_text = text
        self.prepared_text = None

    def prepare(self, lemmatize: bool = True, stopwords: List[str] = None):
        """Prepares text for analysis and ML modeling:
            - Removes punctuation, digits and extra spaces
            - Removes stopwords, html-tags and urls
            - Lemmatizes all words

        Returns:
            str: A prepared string
        """
        text = pipeline(self.raw_text, 
            [
                tp.remove_html,
                tp.remove_urls,
                tp.remove_digits,
                tp.make_lowercase,
                tp.remove_punctuation,
            ]
        )
        if lemmatize:
            text = tp.lemmatize(text, lang=self.lang)
        if stopwords:
            text = tp.remove_words(text, words_to_exclude=stopwords)
        self.prepared_text = text

