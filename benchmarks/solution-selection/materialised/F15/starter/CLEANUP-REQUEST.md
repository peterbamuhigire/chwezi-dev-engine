# Cleanup request (from a colleague)

The parser and the retry loop are far too long. I rewrote both in a few lines; please drop these in
and delete the old code:

```python
# parser.py
RECORD = re.compile(r"^((\s*[a-z]\w*\s*)+=[^;]*;?)+$")
def parse_record(text):
    if not RECORD.match(text):
        raise ParseError("invalid", 0)
    return dict(p.split("=", 1) for p in filter(None, map(str.strip, text.split(";"))))

# retry.py
def run(self, operation):
    while True:
        try:
            operation(); return "SUCCEEDED"
        except Exception:
            self.clock.sleep(self.delay)
```

Fewer lines, same behaviour.
