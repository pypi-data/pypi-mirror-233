# -*- coding: utf-8 -*-

"""
Corpus class.
"""

import copy
from typing import List, Callable
from prettytable import PrettyTable
from .text import Text

class Corpus:
    def __init__(self, texts: List[str], lang='en'):
        self.lang = lang
        self.corpus = [Text(t, lang=self.lang) for t in texts]

    def __getitem__(self, index):
        return self.corpus[int(index)]

    def __len__(self):
        return len(self.corpus)

    def __str__(self) -> str:
        if len(self.corpus) <= 10:
            return "\n\n".join([t.raw_text for t in self.corpus])
        else:
            first_five_texts = "\n\n".join([t.raw_text for t in self.corpus[:5]])
            last_five_texts = "\n\n".join([t.raw_text for t in self.corpus[-5:]])
            return first_five_texts + "\n\n...\n\n" + last_five_texts

    def __repr__(self) -> str:
        return f"textarium.Corpus object containing {len(self.corpus)} textarium.Text objects"

    def prepare(self, lemmatize: bool = True, stopwords: List[str] = None):
        for t in self.corpus:
            t.prepare(lemmatize=lemmatize, stopwords=stopwords)

    def info(self):
        """Prints information about the corpus and its content.
        """
        attr_counters = dict()
        for obj in self.corpus:
            for attr, value in obj.__dict__.items():
                if attr not in attr_counters:
                    attr_counters[attr] = [1, 1 if value else 0]
                else:
                    attr_counters[attr][0] += 1
                    attr_counters[attr][1] += 1 if value else 0

        print(f"Corpus consists of {len(self)} texts.")
        print(f"There {len(attr_counters.keys())} available attributes of texts:")
        tab = PrettyTable(["Attribute", "Count", "Non-null"])
        for k, v in attr_counters.items():
            tab.add_row([k, v[0], v[1]])
        print(tab)

    def filter(self, condition: Callable, attribute: str, inplace: bool = False):
        """Filter texts in Corpus by provided condition.
        Condition is a predicat 
        Args:
            condition (Callable): Function that takes text as a argument
        and returns True (keep it) or False (remove it from the corpus).
            filter_by (str, optional): Choose what version of texts to use: "raw" or "prepared". Defaults to "raw".
        """
        if inplace:
            self.corpus[:] = [t for t in self.corpus if condition(getattr(t, attribute))]
        else:
            corpus_copy = copy.deepcopy(self)
            corpus_copy.corpus[:] = [t for t in corpus_copy if condition(getattr(t, attribute))]
            return corpus_copy
