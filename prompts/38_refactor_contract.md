# refactor_contract

The WORKING (but ugly) code below produces a spending report. Refactor it to a
new two-function API while preserving the output behavior EXACTLY.

Old code (correct, do not ship it):

```python
def do_rep(d):
    if len(d) == 0:
        return "no data"
    t = 0
    u = {}
    for x in d:
        t = t + x["amt"]
        if x["user"] in u:
            u[x["user"]] = u[x["user"]] + x["amt"]
        else:
            u[x["user"]] = x["amt"]
    s = "TOTAL " + str(t) + "\n"
    ks = sorted(u.keys())
    for k in ks:
        s = s + k + " " + str(u[k]) + "\n"
    a = t / len(d)
    s = s + "AVG " + ("%.1f" % a)
    return s
```

New API (entries are dicts like {"user": "zoe", "amt": 30}, amounts are ints):

    def summarize(entries: list) -> dict
        returns {"count": <len>, "total": <sum>, "by_user": {user: user_total},
                 "avg": <float mean, 0.0 for empty>}

    def render(summary: dict) -> str
        renders ANY well-formed summary dict (it must not recompute from
        entries): "no data" when count is 0; otherwise the exact old format -
        TOTAL line, one line per user sorted by name, AVG with one decimal,
        newline-separated, no trailing newline.

render(summarize(x)) must equal the old do_rep(x) for every input.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
