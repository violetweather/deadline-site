# legacy_cleanup

The legacy function below parses a config format. It is buggy and gross.
Rewrite it CLEAN and CORRECT per the spec. Return the complete module with:

    def parse_config(text: str) -> dict

SPEC (the legacy code violates several of these):
- Lines are processed top to bottom. Leading/trailing whitespace is stripped.
- An inline comment starts at the FIRST occurrence of " #" (space then hash)
  and runs to end of line; strip it (and trailing spaces) BEFORE other rules.
  A "#" without a space before it is literal data.
- After stripping: empty lines and lines starting with "#" are skipped.
- "[name]" starts a section; keys inside get the prefix "name." (whitespace
  inside the brackets is stripped). An empty section name raises ValueError.
- Other lines must be "key = value" (split on the FIRST "="): key is stripped
  (empty key -> ValueError), value is stripped. A line with no "=" raises
  ValueError.
- Values: exactly "true"/"false" (lowercase) -> Python bool; else if int(value)
  parses -> int; else the string.
- Duplicate keys: the LAST occurrence wins. Calls must be independent (no
  state carried between calls).

Legacy code:

```python
CACHE = {}

def parse_config(text):
    if text in CACHE:
        return CACHE[text]
    out = {}
    sec = ""
    for line in text.split("\n"):
        line = line.split("#")[0].strip()
        if line == "":
            continue
        if line[0] == "[":
            sec = line[1:-1]
            continue
        k, v = line.split("=")
        k = k.strip()
        if sec != "":
            k = sec + "." + k
        v = v.strip()
        if v.capitalize() == "True":
            v = True
        elif v.capitalize() == "False":
            v = False
        elif v.isdigit():
            v = int(v)
        if k not in out:
            out[k] = v
    CACHE[text] = out
    return out
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
