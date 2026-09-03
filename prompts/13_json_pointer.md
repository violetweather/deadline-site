# json_pointer

Write a Python function:

    def resolve(doc, pointer: str)

Resolve a JSON-Pointer-style path against doc (nested dicts and lists).

Rules:
- pointer "" returns doc itself.
- Otherwise pointer must start with "/", else raise ValueError.
- Split the rest on "/". In each token, unescape "~1" to "/" first, then "~0" to "~".
- On a dict: look up the unescaped token as a key. Missing key -> raise KeyError.
- On a list: the RAW token must be all digits with no leading zero ("0" is fine),
  else raise ValueError. Index out of range -> raise IndexError.
- Descending into anything that is not a dict or list -> raise KeyError.

Examples:
- resolve({"a": {"b": [10, 20]}}, "/a/b/1") -> 20
- resolve({"a/b": 1}, "/a~1b") -> 1

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
