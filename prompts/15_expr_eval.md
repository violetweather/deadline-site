# expr_eval

Write a Python function:

    def ev(s: str) -> int

Evaluate an integer arithmetic expression string.

Rules:
- Operators: + - * / and parentheses. Usual precedence (* / before + -),
  left-to-right within the same level.
- / is FLOOR division: it rounds toward negative infinity, like Python's //.
  So ev("-7/2") == -4.
- Unary minus is allowed before a number or "(" (e.g. "-4", "2*-3", "-(1+2)").
- Number literals are non-negative integers. Whitespace may appear anywhere.
- Division by zero raises ZeroDivisionError.
- Any malformed input (empty string, unbalanced parens, trailing junk,
  unknown characters) raises ValueError.

Examples: ev("1+2*3") -> 7, ev("(1+2)*3") -> 9, ev("-(2+3)*2") -> -10

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
