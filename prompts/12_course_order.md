# course_order

Write a Python function:

    def order(n: int, prereqs: list) -> list

There are n courses numbered 0 .. n-1. Each prereq is a list [a, b] meaning
course b must be taken BEFORE course a. Return a list of all n courses in a
valid order. When several courses are available at the same time, always pick
the lowest course number first. If no valid order exists (a cycle), return [].

Examples:
- order(4, [[1,0],[2,0],[3,1],[3,2]]) -> [0, 1, 2, 3]
- order(2, [[0,1],[1,0]]) -> []

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
