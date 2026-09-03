# exact_ledger

Write a Python function:

    def process(ops: list) -> list

A money ledger. Balance starts at 0.00 and is EXACT to the cent - any
floating-point sloppiness will fail. For each operation string, append one
output string to the result: the new balance formatted "D.CC" (no thousands
separators, cents always two digits), or "REJECTED" (balance unchanged).

Operations:
- "DEP <amount>"  deposit. Amount format: digits, ".", exactly two digits
  (e.g. "12.34"). Anything else raises ValueError.
- "WD <amount>"   withdraw. If amount > balance, the op is REJECTED.
- "FEE <p>%"      charge a fee of p percent of the CURRENT balance, where p is
  digits with an optional fraction of 1-3 digits (e.g. "1.5%", "0.125%").
  The fee in cents is rounded HALF-TO-EVEN (banker's rounding: an exact
  half-cent rounds to the nearest EVEN number of cents). If the rounded fee
  exceeds the balance, REJECTED.
- "INT <p>%"      interest: computed exactly like FEE but ADDED to the balance.
- Any other operation, or a malformed argument, raises ValueError.

Examples:
- process(["DEP 4.00", "FEE 0.125%"]) -> ["4.00", "4.00"]
  (fee is exactly half a cent; 0 is even, so it rounds to 0)
- process(["DEP 12.00", "FEE 0.125%"]) -> ["12.00", "11.98"]
  (fee is 1.5 cents; ties go to even, so 2)

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
