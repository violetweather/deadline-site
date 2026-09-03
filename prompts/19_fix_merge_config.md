# fix_merge_config

The function below deep-merges two config dicts. Required behavior:
- Return a NEW dict. Neither input may be mutated, at any depth.
- Mutating the returned dict (at any depth) must never change either input.
- When both sides hold a dict for the same key, merge recursively.
- Otherwise the override value wins (lists and scalars are replaced, not merged).

The current version breaks the first two rules. Fix it. Return the complete
fixed module.

```python
def merge(base, override):
    result = base
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = merge(result[k], v)
        else:
            result[k] = v
    return result
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
