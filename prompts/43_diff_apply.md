# diff_apply

Write a Python function:

    def apply(lines: list, hunks: list) -> list

Apply patch hunks to a list of text lines. Each hunk is a dict:
{"start": int, "remove": [lines], "insert": [lines]}.

Rules (validate ALL hunks before changing anything):
- "start" is a 1-based line number in the ORIGINAL list. Not an int >= 1
  -> ValueError.
- Hunks must be in ascending order and must not overlap: each hunk's start
  must be strictly greater than the previous hunk's last removed position
  (for an insert-only hunk, its position counts as start - 1).
  Violations -> ValueError.
- The "remove" lines must match the original lines at that position exactly,
  or ValueError ("context mismatch"). remove may reach at most the end of
  the list.
- An insert-only hunk (remove == []) inserts BEFORE line `start`;
  start == len(lines) + 1 appends at the end.
- Return the patched list; the input list must not be mutated.

Example: apply(["a", "b", "c"], [{"start": 2, "remove": ["b"], "insert": ["B", "B2"]}])
-> ["a", "B", "B2", "c"]

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
