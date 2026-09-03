# json_merge

Write a Python function (the json module is expected here):

    def merge_json(docs: list) -> str

docs is a list of JSON strings. Each must parse to a JSON OBJECT (dict) -
anything else, or unparseable JSON, raises ValueError.

Deep-merge the objects in order (later docs win): when both sides hold an
object for the same key, merge recursively; otherwise the later value
replaces the earlier one (arrays are replaced, not concatenated).

Return the result serialized with json.dumps using sort_keys=True and
separators=(",", ":") and everything else left at defaults.

Example: merge_json(['{"a":{"x":1}}', '{"a":{"y":2},"b":[1]}'])
-> '{"a":{"x":1,"y":2},"b":[1]}'

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
