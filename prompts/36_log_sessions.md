# log_sessions

Write a Python function:

    def report(lines: list) -> list

Turn raw log lines into a session report. Every rule below is enforced by
hidden tests - exactness is the task.

Input lines have the form "HH:MM:SS LEVEL module message":
- the timestamp is exactly two digits each, 24-hour, 00:00:00-23:59:59
- LEVEL is one of DEBUG, INFO, WARN, ERROR (severity in that order)
- module is a single token; message is everything after it and may contain
  spaces, but must be non-empty
- timestamps must be NON-DECREASING across the whole input
- any violation raises ValueError

Sessionization (PER MODULE): a line belongs to the module's current session
when its timestamp is at most 900 seconds after the PREVIOUS line of that
same module; a gap of MORE than 900 seconds starts a new session.

Output: for each module in alphabetical order, one line per session in time
order, formatted EXACTLY:

    "{module} {count} events {start}-{end} worst={LEVEL}"

where start/end are the session's first/last timestamps re-formatted as
HH:MM:SS, count is the number of lines in the session (yes, "1 events"),
and worst is the highest-severity level seen in the session.
report([]) -> [].

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
