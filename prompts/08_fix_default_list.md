# fix_default_list

The function below is meant to work like this:
- add_tag("a") called with no list returns a NEW list ["a"] every time.
- add_tag("y", my_list) appends "y" to my_list and returns that same list object.

It has a bug: calls without a list share state between calls.

Fix it. Return the complete fixed module.

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
