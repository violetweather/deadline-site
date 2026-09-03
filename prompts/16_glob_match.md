# glob_match

Write a Python function:

    def match(pattern: str, s: str) -> bool

A glob-style matcher over plain strings (no paths, no escapes, case-sensitive).

Pattern syntax:
- *  matches any sequence of characters, including the empty sequence.
- ?  matches exactly one character.
- [set] matches one character from the set. The set holds plain characters
  and ranges like a-z (inclusive, by character code). If the first character
  after "[" is "!", the set is negated (one character NOT in the set).
- Every other character matches itself.
- An unclosed "[" raises ValueError. Assume "]" never appears inside a set.

Examples:
- match("*.py", "a.py") -> True
- match("a?c", "ac") -> False
- match("[!a-c]x", "dx") -> True

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
