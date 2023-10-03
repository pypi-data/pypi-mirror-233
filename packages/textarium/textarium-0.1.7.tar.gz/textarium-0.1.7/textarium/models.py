# -*- coding: utf-8 -*-

"""
Function for extracting information from texts.
"""

from pymorphy2 import MorphAnalyzer
from nltk.stem import WordNetLemmatizer

morph_ru = MorphAnalyzer()
morph_en = WordNetLemmatizer()