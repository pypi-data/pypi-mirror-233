# -*- coding: utf-8 -*-

"""
Stopwords.
"""

from os import path
from typing import List

def get_stopwords(lang: str = 'en') -> List[str]:
    file_path = path.join(path.dirname(__file__), f'{lang}_stopwords.txt')
    with open(file_path, 'r') as f:
        stopwords = f.readlines()
    return stopwords