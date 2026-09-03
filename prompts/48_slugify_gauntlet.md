# slugify_gauntlet

Write a Python function:

    def slug(title: str, max_len: int = 64) -> str

Turn a title into a URL slug. Simple rules - graded on the corners:

1. max_len < 1 raises ValueError.
2. Lowercase the title. Keep ASCII letters a-z and digits 0-9; EVERY other
   character becomes "-".
3. Collapse runs of "-" into one, then strip leading/trailing "-".
4. If the result is longer than max_len, cut it to max_len characters, then
   strip any trailing "-" the cut exposed.
5. If the result is empty at the end, return "untitled".

Examples: slug("Hello, World!") -> "hello-world";
slug("  !!  ") -> "untitled"; slug("a b c", 3) -> "a-b"

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
