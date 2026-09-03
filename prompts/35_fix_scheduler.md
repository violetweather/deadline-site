# fix_scheduler

A two-file project. `jobs.py` is given and must NOT be changed:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    jid: str
    priority: int
    deps: tuple = ()
    duration: int = 1
```

`scheduler.py` below contains SEVERAL bugs that interact. Required behavior
of build_schedule(jobs) -> list of (jid, start, end):

- One worker. Time starts at 0. Repeatedly pick, among all READY jobs (jobs
  whose deps have ALL already finished), the one with the HIGHEST priority;
  ties break by SMALLEST jid (string comparison). Run it to completion
  (end = start + duration); the next job starts when it ends.
- Validation happens BEFORE any scheduling: a duplicate jid raises
  ValueError; a duration <= 0 raises ValueError; a dep naming a jid that is
  not in the input raises KeyError.
- If at any point no job is ready but unscheduled jobs remain (a dependency
  cycle), raise ValueError.

Current buggy scheduler.py:

```python
from jobs import Job

def build_schedule(jobs):
    jobs_by_id = {}
    for j in jobs:
        jobs_by_id[j.jid] = j
    done = []
    out = []
    t = 0
    while len(out) < len(jobs):
        ready = []
        for j in jobs:
            if j.jid in done:
                continue
            if all(d in done for d in j.deps):
                ready.append(j)
        ready.sort(key=lambda j: (j.priority, j.jid))
        j = ready[0]
        out.append((j.jid, t, t + j.duration))
        done.append(j.jid)
        t += j.duration
    return out
```

Reply with the complete fixed `scheduler.py` (it may `from jobs import Job`).

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
