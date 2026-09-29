from worker.errors import ParseError


def _is_valid_key(key):
    if key == "":
        return False
    first = key[0]
    if not ("a" <= first <= "z"):
        return False
    for character in key[1:]:
        if "a" <= character <= "z":
            continue
        if "0" <= character <= "9":
            continue
        if character == "_":
            continue
        return False
    return True


def parse_record(text):
    if text is None:
        raise ParseError("empty", 0)
    if text.strip() == "":
        raise ParseError("empty", 0)
    result = {}
    pieces = text.split(";")
    position = 0
    for piece in pieces:
        stripped = piece.strip()
        if stripped == "":
            if position == len(pieces) - 1:
                break
            else:
                raise ParseError("missing_separator", position)
        if "=" not in stripped:
            raise ParseError("missing_separator", position)
        else:
            key_part, value_part = stripped.split("=", 1)
            key = key_part.strip()
            value = value_part.strip()
            if not _is_valid_key(key):
                raise ParseError("bad_key", position)
            else:
                if key in result:
                    raise ParseError("duplicate_key", position)
                else:
                    result[key] = value
        position = position + 1
    return result
