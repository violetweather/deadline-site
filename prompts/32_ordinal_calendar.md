# ordinal_calendar

Implement a made-up calendar. Do not reach for datetime - it cannot help you.

The Deadline calendar:
- Years are numbered 0, 1, 2, ... A year has 13 months, numbered 1..13.
- Months 1..12 always have 28 days. Month 13 has 28 days, or 29 days in a
  LEAP year. A year is leap when it is divisible by 5 but NOT divisible by 40.
- Day numbers within a month start at 1.
- Absolute day 0 is year 0, month 1, day 1. Days count up forever.
- Weekdays cycle through exactly 8 names, in order:
  ["Aday","Bday","Cday","Dday","Eday","Fday","Gday","Hday"], and absolute
  day 0 is an "Aday".

Write THREE functions:

    def to_ordinal(y: int, m: int, d: int) -> int
        Absolute day number of a date. Invalid dates (y < 0, month out of
        range, day out of range for that month/year) raise ValueError.

    def from_ordinal(n: int) -> tuple
        The (y, m, d) tuple for absolute day n. Negative n raises ValueError.

    def weekday(n: int) -> str
        Weekday name of absolute day n. Negative n raises ValueError.

Examples: to_ordinal(0, 1, 1) -> 0; weekday(0) -> "Aday"; year 0 is NOT leap
(0 is divisible by 40).

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
