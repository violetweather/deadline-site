# weighted_meetings

Write a Python function:

    def best_value(meetings: list) -> int

Each meeting is a list [start, end, value] of ints with start < end and value > 0.
Pick a subset of meetings so that no two overlap, maximizing the total value.
Meetings that touch (one ends exactly when the next starts) do NOT overlap.
The input list is not sorted. Return the maximum total value (0 for no meetings).

Examples:
- best_value([[1,3,5],[3,6,5]]) -> 10
- best_value([[1,10,10],[2,3,4],[4,5,4],[6,7,4]]) -> 12

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
