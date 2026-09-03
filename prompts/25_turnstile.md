# turnstile

Write a Python function:

    def run(events: list) -> tuple

A state machine starting in state "LOCKED". Process events in order and
collect one output string per event. Return (final_state, outputs) as a
tuple of (str, list).

Transition table (state + event -> new state, output):

| State    | Event | New state | Output   |
|----------|-------|-----------|----------|
| LOCKED   | coin  | UNLOCKED  | unlock   |
| LOCKED   | push  | ALARM     | alarm!   |
| LOCKED   | reset | LOCKED    | reset    |
| UNLOCKED | coin  | UNLOCKED  | refund   |
| UNLOCKED | push  | LOCKED    | lock     |
| UNLOCKED | reset | LOCKED    | reset    |
| ALARM    | coin  | ALARM     | refund   |
| ALARM    | push  | ALARM     | alarm!   |
| ALARM    | reset | LOCKED    | reset    |

Any other event raises ValueError.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
