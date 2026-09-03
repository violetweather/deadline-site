# fix_chunks

The function below must split a list into consecutive chunks of size n.
The last chunk may be smaller. n <= 0 must raise ValueError.

It has a bug: it drops items. Fix it. Return the complete fixed module.

```python
def chunks(items, n):
    out = []
    for i in range(0, len(items) - n, n):
        out.append(items[i:i+n])
    return out
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
