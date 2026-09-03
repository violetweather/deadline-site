# tinydb

The long one. Write a Python function:

    def run_session(lines: list) -> list

A tiny transactional key-value store driven by command lines. Process the
lines in order and return EXACTLY one output string per line. Four layers of
rules; everything interacts, and the hidden tests grade each layer.

TOKENIZING. Tokens are separated by one or more spaces. A token is either
- bare: any run of non-space characters; a '"' anywhere inside a bare token
  is a syntax error; or
- quoted: "..." where \" stands for a quote and \\ for a backslash; a
  backslash before anything else, an unclosed quote, or a closing quote not
  followed by a space or the end of the line is a syntax error.
An empty/whitespace-only line, any tokenizing failure, or a line not matching
a command form below produces the output "ERR syntax" for that line
(processing continues with the next line).

COMMANDS (argument counts are exact):
- SET k v      store string v under key k -> "OK"
- GET k        -> the value, or "NULL" if unset
- DEL k        if k currently has a value: remove it -> "1"; else -> "0"
- INCR k       if k is unset: store "1" -> "1". Otherwise, if Python's
               int(value) accepts the stored string: store str(int(value)+1)
               and output it; if int() raises -> "ERR type" (store unchanged)
- BEGIN        open a transaction -> "OK". Transactions NEST.
- COMMIT       merge the innermost transaction into its parent -> "OK";
               with no open transaction -> "ERR no tx"
- ROLLBACK     discard the innermost transaction entirely -> "OK";
               with no open transaction -> "ERR no tx"
- SNAPSHOT     serialize every currently-visible key, sorted, as k=v pairs
               joined by ";". In BOTH keys and values escape backslash as
               \\, ";" as \;, and "=" as \=. If nothing is visible -> "EMPTY"

TRANSACTION SEMANTICS. Reads (GET, INCR's read, DEL's check, SNAPSHOT) see
through all open transactions, innermost first. Writes and deletes land in
the innermost open transaction only. A DEL inside a transaction hides any
outer value until that transaction is rolled back; committing it makes the
delete real.

Example session:
    run_session(["SET a 1", "BEGIN", "INCR a", "GET a", "ROLLBACK", "GET a"])
    -> ["OK", "OK", "2", "2", "OK", "1"]

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
