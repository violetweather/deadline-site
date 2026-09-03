# lru_cache

Write a Python class:

    class LRU:
        def __init__(self, capacity: int): ...
        def get(self, key): ...
        def put(self, key, value): ...

A least-recently-used cache holding at most `capacity` entries.

Rules:
- get(key): return the stored value and refresh the key's recency. If the key
  is missing, return None. Track counters: self.hits and self.misses (ints).
- put(key, value): insert or update; both refresh recency. If inserting pushes
  the cache over capacity, evict the least recently used key.
- Keep self.evicted: a list of evicted keys in eviction order.
- capacity 0 is legal: every put is immediately evicted, nothing is stored.

Example: LRU(2); put(1,"a"); put(2,"b"); get(1); put(3,"c") evicts key 2.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
