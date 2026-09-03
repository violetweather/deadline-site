# fix_binary_search

The function below is meant to do binary search on a sorted list of unique ints.
It must return the index of `target`, or -1 if `target` is not in the list.
It has a bug: on some inputs it never finishes.

Fix it. Return the complete fixed module.

```python
def binary_search(items, target):
    lo, hi = 0, len(items)
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid
        else:
            hi = mid
    return -1
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
