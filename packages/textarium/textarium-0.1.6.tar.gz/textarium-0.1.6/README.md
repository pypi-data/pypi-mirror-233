# textarium: easy-to-use Python package for text analysis.
[![PyPI Latest Release](https://img.shields.io/pypi/v/textarium)](https://pypi.org/project/textarium/)
[![License](https://img.shields.io/pypi/l/textarium)](https://github.com/6b656b/textarium/blob/main/LICENSE)
[![Activity](https://img.shields.io/github/commit-activity/m/6b656b/textarium)](https://github.com/6b656b/textarium/pulse)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## What is it?

**textarium** is a Python package that provides flexible text analysis functions designed to 
make text analysis intuitive and easy. It aims to be the high-level tool for
preparing text-data and complex analysis or NLP modeling.

## Installation
Binary installer for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/textarium).

```sh
# Type this in your command-line
pip install textarium
```

## Getting started

```py
from textarium import Text
import nltk
nltk.download('wordnet')

s = "This a text example. You can preprocess and analyze it with this package."
text = Text(s, lang='en')
text.prepare()

print(text.prepared_text)
```

## Documentation
The official documentation is hosted on Github.io: https://6b656b.github.io/textarium
## License
[MIT](LICENSE)