# service_feature

A four-file project. Three files are GIVEN and must not be changed. You write
the fourth, `service.py`, which must build ON TOP of them.

models.py:
```python
from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    name: str
    price_cents: int
    qty: int
```

store_db.py:
```python
class Db:
    def __init__(self):
        self._rows = {}

    def all(self):
        return [self._rows[k] for k in sorted(self._rows)]

    def get(self, sku):
        return self._rows.get(sku)

    def upsert(self, product):
        self._rows[product.sku] = product

    def delete(self, sku):
        self._rows.pop(sku, None)
```

util.py:
```python
def money(cents):
    return f"${cents // 100}.{cents % 100:02d}"


def valid_sku(sku):
    return isinstance(sku, str) and len(sku) == 6 and sku.isalnum() \
        and sku.upper() == sku
```

Write `service.py` with FOUR functions:

- restock(db, sku, qty): qty <= 0 -> ValueError; util.valid_sku(sku) false
  -> ValueError; sku not in db -> KeyError; else add qty to the product's
  stock and upsert it.
- sell(db, sku, qty): same validations; selling more than the stock ->
  ValueError (stock unchanged); stock may reach exactly 0 (the row stays).
- low_stock(db, threshold): products with qty < threshold, sorted by
  (qty ascending, then sku ascending), each formatted EXACTLY
  "{{sku}} {{name}}: {{qty}} left (worth {{util.money(price_cents * qty)}})".
- total_value(db): sum of price_cents * qty over every product, as an int.

REQUIREMENT: import the modules (`import util`) and call `util.money` and
`util.valid_sku` through the module - the grader swaps them out to check.
Reply with the complete `service.py`.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
