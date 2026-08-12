from __future__ import annotations

import re
import unicodedata
from typing import Any


_SINGLE_ASCII_OR_FULLWIDTH_ALNUM = re.compile(r"^[A-Za-z0-9Ａ-Ｚａ-ｚ０-９]$")


def cell_to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value)).strip()
    return str(value).strip()


def compact_text(text: str) -> str:
    return "".join(str(text).strip().lower().split())


def trim_outer_punctuation(text: str) -> str:
    chars = list(str(text).strip())
    while chars and _is_punctuation_or_symbol(chars[0]):
        chars.pop(0)
    while chars and _is_punctuation_or_symbol(chars[-1]):
        chars.pop()
    return "".join(chars).strip()


def is_all_punctuation_or_symbols(text: str) -> bool:
    stripped = str(text).strip()
    if not stripped:
        return False
    useful_chars = [ch for ch in stripped if not ch.isspace()]
    return bool(useful_chars) and all(_is_punctuation_or_symbol(ch) for ch in useful_chars)


def is_invalid_answer(value: Any) -> bool:
    text = cell_to_text(value)
    if not text:
        return True
    if _SINGLE_ASCII_OR_FULLWIDTH_ALNUM.fullmatch(text):
        return True
    if is_all_punctuation_or_symbols(text):
        return True
    return False


def _is_punctuation_or_symbol(ch: str) -> bool:
    category = unicodedata.category(ch)
    return category.startswith("P") or category.startswith("S")
