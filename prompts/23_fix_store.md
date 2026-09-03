# fix_store

A tiny two-file project. `models.py` is given and must NOT be changed:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    sku: str
    name: str
    price_cents: int
```

`store.py` below is buggy. Required behavior for class Inventory:
- add(item, qty): qty <= 0 raises ValueError. Adding accumulates quantity.
  Adding an item whose sku is already known but whose name or price differs
  from the stored item raises ValueError.
- remove(sku, qty): qty <= 0 raises ValueError. Unknown sku raises KeyError.
  Removing more than is held raises ValueError (and changes nothing).
  When a sku's quantity reaches exactly 0, the sku is forgotten entirely
  (count returns 0, remove afterwards raises KeyError).
- count(sku): current quantity, 0 for unknown skus.
- total_value_cents(): sum of price_cents * quantity over everything held.

Current buggy store.py:

```python
from models import Item

class Inventory:
    def __init__(self):
        self._items = {}
        self._counts = {}

    def add(self, item, qty):
        self._items[item.sku] = item
        self._counts[item.sku] = self._counts.get(item.sku, 0) + qty

    def remove(self, sku, qty):
        self._counts[sku] -= qty

    def count(self, sku):
        return self._counts.get(sku, 0)

    def total_value_cents(self):
        return sum(self._items[s].price_cents for s in self._counts)
```

Reply with the complete fixed `store.py` (it may `from models import Item`).

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
