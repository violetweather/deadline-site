# fix_flatten_cycle

The function below flattens arbitrarily nested lists depth-first.
Required behavior:
- flatten([1, [2, [3]], 4]) -> [1, 2, 3, 4]
- The SAME list appearing twice (sharing) is fine and flattened twice.
- If the structure contains a CYCLE (a list that contains itself, directly
  or indirectly), raise ValueError instead of recursing forever.

The current version hangs on cycles. Fix it. Return the complete fixed module.
The function must still be callable as flatten(x) with one argument.

```python
def flatten(x):
    out = []
    for item in x:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
