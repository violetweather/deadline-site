# report_module

A two-file project. `utils.py` is given and must NOT be changed:

```python
def mean(nums):
    return sum(nums) / len(nums) if nums else 0.0


def by_key(rows, key):
    out = {}
    for row in rows:
        out.setdefault(row[key], []).append(row)
    return out
```

Write `report.py` with one function:

    def summarize(rows: list) -> dict

rows is a list of dicts like {"team": "red", "points": 10}.

Return:
- {"teams": ..., "best_team": ..., "overall_avg": ...}
- "teams": dict mapping each team to {"games": <row count>, "avg": <mean of
  its points, rounded to 2 decimals>}
- "best_team": the team with the highest avg; ties break alphabetically
  (lowest name wins).
- "overall_avg": mean of ALL points, rounded to 2 decimals.
- Empty rows -> {"teams": {}, "best_team": None, "overall_avg": 0.0}

REQUIREMENT: import the module (`import utils`) and call `utils.mean(...)`
and `utils.by_key(...)` for the math/grouping. Do not re-implement them and
do not use `from utils import ...` (the grader checks module-level calls).

Reply with the complete `report.py`.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
