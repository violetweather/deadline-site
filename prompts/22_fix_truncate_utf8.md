# fix_truncate_utf8

The function below must return the LONGEST PREFIX of s whose UTF-8 encoding
is at most max_bytes bytes. It must never split a multi-byte character.
max_bytes is >= 0.

The current version crashes when the cut lands inside a multi-byte character.
Fix it. Return the complete fixed module.

```python
def truncate_utf8(s, max_bytes):
    return s.encode("utf-8")[:max_bytes].decode("utf-8")
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
