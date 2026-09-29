"""Linear-time parser for ``key=value;key=value`` records (see README.md for the error codes)."""
import re

from worker.errors import ParseError

# Anchored, no nested quantifiers: fullmatch on one key is linear.
KEY_PATTERN = re.compile(r"[a-z][a-z0-9_]*")


def parse_record(text):
    if text is None or not text.strip():
        raise ParseError("empty", 0)
    pairs = text.split(";")
    if pairs[-1].strip() == "":
        pairs.pop()  # a single trailing separator is allowed
    result = {}
    for position, pair in enumerate(pairs):
        key, separator, value = pair.partition("=")
        if not separator:
            raise ParseError("missing_separator", position)
        key = key.strip()
        if not KEY_PATTERN.fullmatch(key):
            raise ParseError("bad_key", position)
        if key in result:
            raise ParseError("duplicate_key", position)
        result[key] = value.strip()
    return result
