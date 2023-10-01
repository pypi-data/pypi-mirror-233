# -*- coding: utf-8 -*-

"""
Importable constants value.
"""

from .vendor.better_enum import BetterStrEnum


class TokenTypeEnum(BetterStrEnum):
    """
    Token type enum. It will be used to declare a token in a dict.

    Example::

        {
            "type": "Token::Sub",
            "kwargs": {
                "template": "hello {name}",
                "params": {"name": "$name"},
            }
        }

    .. versionadded:: 0.1.1
    """
    raw = "Token::Raw"
    jmespath = "Token::Jmespath"
    sub = "Token::Sub"
    join = "Token::Join"
    split = "Token::Split"
    map = "Token::Map"

TYPE = "type"
