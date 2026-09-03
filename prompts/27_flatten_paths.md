# flatten_paths

Write a Python function:

    def flatten(obj: dict) -> dict

Flatten a nested structure of dicts and lists into a single flat dict mapping
path strings to leaf values.

Rules:
- obj is always a dict at the top level. Keys are strings without dots.
- Dict keys are joined with "." between levels.
- A list element appends "[i]" to the current path, with NO dot before it.
- Anything that is not a dict or list is a leaf and is stored as-is.
- Empty dicts and empty lists produce no entries.

Examples:
- flatten({"a": {"b": 1}}) -> {"a.b": 1}
- flatten({"c": [1, {"d": 2}]}) -> {"c[0]": 1, "c[1].d": 2}
- flatten({"x": [[7]]}) -> {"x[0][0]": 7}

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
