# tiny_regex

Write a Python function:

    def fullmatch(pattern: str, s: str) -> bool

A miniature regex engine, WITH BACKREFERENCES, matched against the ENTIRE
string. Do not use the re module - your engine must implement:

- lowercase letters match themselves; "." matches any one character
- "(...)" is a CAPTURING group; groups are numbered 1, 2, ... by the order
  of their opening parentheses
- "|" is alternation, lowest precedence, allowed at top level and in groups
- "*" repeats the preceding item (a literal, ".", a group, or a backreference)
  zero or more times
- "\\1" .. "\\9" match EXACTLY the text most recently captured by that group.
  A backreference to a group that has not captured anything fails to match.

Malformed patterns raise ValueError: unbalanced parentheses, "*" with nothing
before it, "\\0" or a backreference to a group number that does not exist in
the pattern, or any character outside the syntax above.

Examples:
- fullmatch("(ab)c\\1", "abcab") -> True
- fullmatch("(a|b)\\1", "ab") -> False  (the backref must repeat the capture)
- fullmatch("(a*)b\\1", "aabaa") -> True

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
