# fix_pager

The class below splits a list into pages. Required behavior:

- Pager(items, size): size <= 0 raises ValueError. The pager takes a
  SNAPSHOT of items at construction (later changes to the original list do
  not affect it), and never mutates the input.
- Iterating yields lists of `size` items; the LAST page may be shorter and
  must still be yielded.
- The same Pager can be iterated any number of times, independently, from
  the start each time.
- An empty input yields no pages (cleanly - no crash).

The current version violates all of that. Fix it. Return the complete module.

```python
class Pager:
    def __init__(self, items, size):
        self.items = items
        self.size = size

    def __iter__(self):
        page = []
        while True:
            try:
                page.append(self.items.pop(0))
            except IndexError:
                raise StopIteration
            if len(page) == self.size:
                yield page
                page = []
```

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
