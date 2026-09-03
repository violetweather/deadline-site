# room_conflicts

Write a Python function:

    def conflicts(bookings: list) -> dict

Each booking is a list [room, start, end] (room is a string, start < end ints).
Return a dict mapping EVERY room that appears to the number of conflicting
PAIRS of bookings in that room. Two bookings conflict when their time ranges
overlap; touching (one ends exactly when the other starts) is NOT a conflict.

Examples:
- conflicts([["A",1,5],["A",4,8],["B",1,2]]) -> {"A": 1, "B": 0}
- Three bookings that all overlap each other -> 3 pairs.
- conflicts([]) -> {}

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
