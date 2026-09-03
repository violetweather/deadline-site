# query_engine

Write a Python function:

    def query(rows: list, spec: dict) -> list

A tiny query engine over a list of dicts. spec may contain any of:

- "where": a list of [field, op, value] conditions, ALL of which must hold
  (AND). Ops: "eq", "ne", "lt", "gt", "contains" (value in row[field] - for
  strings or lists). A row MISSING the field simply fails the condition (no
  error). An unknown op raises ValueError.
- "order_by": a list of [field, direction] pairs applied as a multi-key sort
  (first pair is the primary key). direction is "asc" or "desc" (anything
  else -> ValueError). Sorting is stable. If any surviving row is missing a
  sort field -> ValueError.
- "select": a list of field names; project each row to exactly those fields
  (a missing field here raises KeyError).
- "limit": keep at most this many rows (applied last). Not an int >= 0 ->
  ValueError.

Apply in the order: where, order_by, select, limit. Missing spec keys mean
"skip that stage". Never mutate the input rows.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
