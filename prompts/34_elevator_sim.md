# elevator_sim

Write a Python function:

    def run(requests: list) -> list

Simulate one elevator, tick by tick, following THIS algorithm literally -
not how you think elevators should work.

Setup: integer time ticks t = 0, 1, 2, ... The elevator starts at floor 1
with doors closed. `requests` is a list of (tick, floor) tuples, already
sorted by tick (same-tick requests keep their list order); if the list is
NOT sorted by tick, raise ValueError.

At every tick t, do these steps in this exact order:
1. Append every request whose tick == t to the pending list, in input order.
2. Then do exactly ONE of the following:
   a. If the door timer is > 0: decrement it. Nothing else happens.
   b. Else if the CURRENT floor appears in the pending list: record a stop
      (t, floor), remove ALL pending entries for that floor, and set the
      door timer to 2.
   c. Else if the pending list is not empty: the target is the pending floor
      that was added EARLIEST (the front of the list - NOT the nearest
      floor). Move exactly one floor toward it.
   d. Else: idle.
The simulation ends when no future requests remain, the pending list is
empty, and the doors are closed. Return the list of recorded stops.

Note the consequences and implement them faithfully: the elevator stops at
any pending floor it passes through, and a request for the floor it is
sitting on (with doors closed) is served the same tick it arrives.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
