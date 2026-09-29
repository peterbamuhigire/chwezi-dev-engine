"""Canonical customer identifiers: the single shared normalisation contract.

Rules for ``canonical_id``:

1. The input must be a ``str``; anything else raises ``TypeError``.
2. Unicode NFC normalisation is applied. NFKC is deliberately *not* used: compatibility
   characters such as the ligature U+FB01 or the circled digit U+2460 are distinct identifiers
   and must stay distinct.
3. Leading and trailing Unicode whitespace is removed; each internal run of whitespace becomes
   a single hyphen.
4. ASCII letters are upper-cased. Non-ASCII letters keep their case, so U+00DF never becomes
   "SS" and two different customers never collapse into one identifier.
5. An empty result raises ``EmptyIdentifierError`` (a ``ValueError``).
"""
from __future__ import annotations

import re
import unicodedata

__all__ = ["EmptyIdentifierError", "canonical_id"]


class EmptyIdentifierError(ValueError):
    """Raised when an identifier is empty after normalisation."""


_WHITESPACE = re.compile(r"\s+")
_ASCII_UPPER = str.maketrans("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def canonical_id(raw: str) -> str:
    if not isinstance(raw, str):
        raise TypeError("customer identifier must be a str")
    text = unicodedata.normalize("NFC", raw).strip()
    if not text:
        raise EmptyIdentifierError("customer identifier is empty")
    return _WHITESPACE.sub("-", text).translate(_ASCII_UPPER)
