# rate_limiter

Write a Python class:

    class RateLimiter:
        def __init__(self, max_events: int, window: float): ...
        def allow(self, t: float) -> bool

A sliding-window rate limiter. allow(t) is called with NON-DECREASING
timestamps and returns True (event allowed) or False (rejected).

Rules:
- An event at time t is allowed if the number of PREVIOUSLY ALLOWED events
  with timestamp strictly greater than (t - window) is less than max_events.
- Only allowed events count against the limit; rejected calls leave no trace.
- An event exactly `window` old has expired (strictly-greater rule).

Example (max 2, window 10): allow(0) True, allow(1) True, allow(2) False,
allow(10) True (the event at 0 has expired at t=10).

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
