# merge_intervals

Write a Python function:

    def merge(intervals: list) -> list

Input: a list of intervals. Each interval is a list [start, end] of ints, start <= end.
The input list is NOT necessarily sorted.
Merge all overlapping intervals. Intervals that touch at an endpoint
(like [1,2] and [2,3]) also merge.
Return a list of [start, end] lists, sorted by start.

Examples:
- merge([[1,3],[2,6],[8,10],[15,18]]) -> [[1,6],[8,10],[15,18]]
- merge([[1,4],[4,5]]) -> [[1,5]]
- merge([]) -> []

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
