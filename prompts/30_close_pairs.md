# close_pairs

Write a Python function:

    def close_pairs(a: list) -> int

Count the pairs of indices (i, j) with i < j such that a[i] XOR a[j] has AT
MOST one bit set - that is, the two values are equal, or they differ in
exactly one bit position.

Constraints:
- 0 <= a[k] < 2**30 for every element.
- len(a) can be up to 200,000, and the hidden tests include a list that big.
- PERFORMANCE IS PART OF THE SPEC: a quadratic solution that compares every
  pair will time out and score zero. Your solution must handle 200,000
  elements in a few seconds.

Examples:
- close_pairs([1, 1]) -> 1        (equal)
- close_pairs([1, 0]) -> 1        (differ in bit 0)
- close_pairs([1, 2]) -> 0        (differ in two bits)
- close_pairs([0, 1, 2, 3]) -> 4

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
