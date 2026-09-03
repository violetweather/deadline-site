# csv_parse

Write a Python function:

    def parse(text: str) -> list

Parse CSV text into a list of rows; each row is a list of field strings.

Rules:
- Fields are separated by commas. Rows are separated by "\n" (no "\r" handling).
- A field MAY be quoted with double quotes. Quotes are only special when the
  quote is the FIRST character of a field. Inside a quoted field, "" means one
  literal quote, and commas and newlines are literal.
- After a quoted field's closing quote, the next character must be a comma,
  a newline, or the end of the text; anything else raises ValueError.
- A quote in the middle of an unquoted field is a literal character.
- A trailing newline at the very end does not create an extra row.
- A blank line produces an empty row: [].
- parse("") returns [].
- An unclosed quote raises ValueError.

Examples:
- parse('a,b\nc,d') -> [["a","b"],["c","d"]]
- parse('"he said ""hi""",x') -> [['he said "hi"', "x"]]

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
