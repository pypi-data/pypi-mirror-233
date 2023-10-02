# -*- coding: utf-8 -*-

"""
Function for extracting information from texts.
"""

import re
import string
from typing import List, Tuple
from razdel import sentenize
from nltk import tokenize
from nltk.util import ngrams
from datetime import datetime
from dateutil import parser
from textarium.utils import date_parser_jumpwords, date_parser_keywords
import textarium.preprocessing as preprocessing

def extract_words(text: str) -> List[str]:
    """Extract a list of tokens from a text

    Args:
        text (str): Any string

    Returns:
        List[str]: A list of extracted tokens
    """
    words = tokenize.word_tokenize(text)
    return words

def extract_sentences(text: str, lang='en') -> List[str]:
    """Extract a list of sentences from a text

    Args:
        text (str): Any string in English or Russian
        lang (str): Text language ('ru' - Russian or 'en' - English)

    Returns:
        List[str]: A list of extracted sentences
    """
    if lang == 'en':
        sentences = tokenize.sent_tokenize(text)
        sentences = [preprocessing.remove_extra_spaces(s) for s in sentences]
    elif lang == 'ru':
        sentences = [i.text for i in sentenize(text)]
    return sentences

def extract_urls(text: str) -> List[str]:
    """Extract a list of URLs from a text

    Args:
        text (str): Any string

    Returns:
        List[str]: A list of extracted URLs
    """
    url_regex = re.compile(
        "((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", re.DOTALL
    )
    parsed_url_objects = re.findall(url_regex, text)
    urls = [url_param[0].strip(string.punctuation) for url_param in parsed_url_objects]
    return urls

def extract_emails(text: str) -> List[str]:
    """Extract a list of E-mails from a text

    Args:
        text (str): Any string

    Returns:
        List[str]: A list of extracted E-mails
    """
    email_regex = re.compile(
        "[a-zA-Z0–9._%+-]+@[a-zA-Z0–9.-]+\.[a-zA-Z]{2,}", re.DOTALL
    )
    parsed_email_objects = re.findall(email_regex, text)
    return parsed_email_objects

def extract_dates(text: str) -> List[datetime]:
    """Extract a list of dates (datetime.datetime)

    Args:
        text (str): Any string

    Returns:
        List[datetime]: A list of dates
    """
    def is_valid_kw(s):
        try:  # is it a number?
            float(s)
            return True
        except ValueError:
            return s.lower() in date_parser_keywords

    def _split(s):
        kw_found = False
        tokens = parser._timelex.split(s)
        for i in range(len(tokens)):
            if tokens[i] in date_parser_jumpwords:
                continue 
            if not kw_found and is_valid_kw(tokens[i]):
                kw_found = True
                start = i
            elif kw_found and not is_valid_kw(tokens[i]):
                kw_found = False
                yield "".join(tokens[start:i])
        if kw_found:
            yield "".join(tokens[start:])
    return [parser.parse(x) for x in _split(text)]

def extract_ngrams(text: str, n: int) -> List[Tuple]:
    """Extract a list of ngrams (tuples of a given length)

    Args:
        text (str): Any string
        n (int): A number of words in ngram

    Returns:
        List[Tuple]: A list of extracted ngrams
    """
    return list(ngrams(extract_words(text), n))