# -*- coding: utf-8 -*-

"""
Corpus class.
"""
from typing import List, Callable
from .text import Text

class Corpus:
    def __init__(self, texts: List[str], lang='en'):
        self.lang = lang
        self.corpus = [Text(t, lang=self.lang) for t in texts]

    def __str__(self) -> str:
        first_five_texts = "\n\n".join([t.raw_text for t in self.corpus[:5]])
        last_five_texts = "\n\n".join([t.raw_text for t in self.corpus[-5:]])
        return first_five_texts + "\n\n...\n\n" + last_five_texts

    def __repr__(self) -> str:
        return f"textarium.Corpus object containing {len(self.corpus)} textarium.Text objects"

    def prepare(self, lemmatize: bool = True, stopwords: List[str] = None):
        for t in self.corpus:
            t.prepare(lemmatize=lemmatize, stopwords=stopwords)

    def filter(self, condition: Callable, filter_by: str = "raw"):
        """Filter texts in Corpus by provided condition.
        Condition is a predicat 
        Args:
            condition (Callable): Function that takes text as a argument
        and returns True (keep it) or False (remove it from the corpus).
            filter_by (str, optional): Choose what version of texts to use: "raw" or "prepared". Defaults to "raw".
        """
        if filter_by == "raw":
            self.corpus[:] = [t for t in self.corpus if condition(t.raw_text)]
        elif filter_by == "prepared":
            self.corpus[:] = [t for t in self.corpus if condition(t.prepared_text)]