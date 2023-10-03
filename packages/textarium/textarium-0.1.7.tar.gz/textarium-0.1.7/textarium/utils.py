# -*- coding: utf-8 -*-

"""
Utility functions
"""

from functools import reduce
from typing import Any, Callable, Sequence
import itertools
from dateutil import parser

def pipeline(
        arg: Any,
        function_pipeline: Sequence[Callable],
) -> Any:
    """A generic Unix-like pipeline

    Args:
        arg (Any): The value you want to pass through a pipeline
        function_pipeline (Sequence[Callable]): An ordered 
        list of functions that comprise your pipeline

    Returns:
        Any: A result of functions pipeline
    """
    return reduce(lambda v, f: f(v), function_pipeline, arg)


date_parser_jumpwords = set(parser.parserinfo.JUMP)
date_parser_keywords = set(kw.lower() for kw in itertools.chain(
    parser.parserinfo.UTCZONE,
    parser.parserinfo.PERTAIN,
    (x for s in parser.parserinfo.WEEKDAYS for x in s),
    (x for s in parser.parserinfo.MONTHS for x in s),
    (x for s in parser.parserinfo.HMS for x in s),
    (x for s in parser.parserinfo.AMPM for x in s),
))