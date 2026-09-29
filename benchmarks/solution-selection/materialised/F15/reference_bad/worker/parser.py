import re

from worker.errors import ParseError

RECORD = re.compile(r"^((\s*[a-z]\w*\s*)+=[^;]*;?)+$")


def parse_record(text):
    if not text or not RECORD.match(text):
        raise ParseError("invalid", 0)
    return {k.strip(): v.strip() for k, v in (p.split("=", 1) for p in filter(None, map(str.strip, text.split(";"))))}
