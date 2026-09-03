# fix_average

The function below must return the arithmetic mean of a list of numbers as a float.
For an empty list it must return 0.0 (not crash).

It has a bug: it crashes on an empty list.

Fix it. Return the complete fixed module.

```python
def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
