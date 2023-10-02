# -*- coding: utf-8 -*-

"""
Methods for calculating different statistics for a Text object.
"""
from typing import List, Union, Callable, Optional
from textarium import (
    extract_words,
    extract_sentences,
    extract_urls,
    remove_punctuation,
    remove_digits,
)

def characters_count(text: str) -> int:
    return len(text)

def words_count(text: str) -> int:
    return len(extract_words(remove_punctuation(text)))

def unique_words_count(text: str) -> int:
    return len(set(extract_words(remove_punctuation(text))))

def sentences_count(text: str) -> int:
    return len(extract_sentences(text))

def urls_count(text: str) -> int:
    return len(extract_urls(text))

def characters_per_word(text: str) -> float:
    words = extract_words(
        remove_digits(remove_punctuation(text))
    )
    characters_cnt = 0
    for w in words:
        characters_cnt += len(w)
    words_cnt = len(words)
    return characters_cnt / words_cnt

def words_per_sentence(text: str) -> float:
    sentences_cnt = sentences_count(text)
    words_cnt = words_count(text)
    return words_cnt / sentences_cnt

def count_words_by_predicat(text, predicat_func: Callable) -> int:
    words = extract_words(
        remove_digits(remove_punctuation(text))
    )
    words_cnt = 0
    for w in words:
        if predicat_func(w):
            words_cnt += 1
    return words_cnt

def long_words_count(text: str, normalize: bool = False) -> Union[int, float]:
    LONG_WORD_LENGTH = 8
    long_words_cnt = count_words_by_predicat(
        text, predicat_func=lambda x: len(x) >= LONG_WORD_LENGTH
    )
    words_cnt = words_count(text)
    if normalize:
        return long_words_cnt / words_cnt
    else:
        return long_words_cnt

def short_words_count(text: str, normalize: bool = False) -> Union[int, float]:
    SHORT_WORD_LENGTH = 4
    short_words_cnt = count_words_by_predicat(
        text, predicat_func=lambda x: len(x) <= SHORT_WORD_LENGTH
    )
    words_cnt = words_count(text)
    if normalize:
        return short_words_cnt / words_cnt
    else:
        return short_words_cnt

# def lexical_density(text: str, stopwords: List[str], lexical_items: Optional(List[str])):
#     words_cnt = words_count(text)
#     if lexical_items:
#         lexical_items = set(lexical_items) - set(stopwords)
#         lexical_items_cnt = count_words_by_predicat(text, lambda x: x in lexical_items)
#     else:
#         lexical_items_cnt = count_words_by_predicat(text, lambda x: x not in stopwords)
#     return lexical_items / words_cnt

def coleman_liau_grade():
    pass

def flesch_kincaid_grade_level():
    pass

def smog_grade():
    pass



