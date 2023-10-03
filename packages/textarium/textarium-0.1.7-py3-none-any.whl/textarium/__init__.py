"""
Textarium
=====

Provides
  1. Classes and functions to process and analyze text information
  2. Collections of stopwords and other useful dictionaries for NLP tasks

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide, available from
`the Textarium homepage <https://6b656b.github.io/textarium/>`_.

See below for further instructions.

Code snippets are indicated by three greater-than signs::

  >>> from textarium import Text
  >>> text = Text("Hello world!", lang='en')
  >>> text.prepare()
  >>> print(text.prepared_text)

Available subpackages
---------------------
extraction
    Basic functions for extracting any kind of tokens from string
models
    NLP models for text preprocessing and embedding
preprocessing
    Functions for text preprocessing
text
    Text class

Viewing documentation using IPython
-----------------------------------

Start IPython and import `textarium`: `import
textarium`.  Then, directly past or use the ``%cpaste`` magic to paste
examples into the shell.  To see which functions are available in `textarium`,
type ``textarium.<TAB>`` (where ``<TAB>`` refers to the TAB key).

"""
from .extraction import extract_words, extract_urls, extract_sentences
from .preprocessing import (
    remove_extra_spaces,
    remove_charset,
    remove_digits,
    remove_html,
    remove_punctuation,
    remove_urls,
    remove_words,
    make_lowercase,
    lemmatize
)
from .text import Text
from .corpus import Corpus

__all__ = [
    "extract_words",
    "extract_urls",
    "extract_sentences",
    "remove_extra_spaces",
    "remove_charset",
    "remove_digits",
    "remove_html",
    "remove_punctuation",
    "remove_urls",
    "remove_words",
    "make_lowercase",
    "lemmatize",
    "Text",
    "Corpus",
]