# table_format

Write a Python function:

    def format_table(headers: list, rows: list) -> str

Input:
- headers: a list of column header strings.
- rows: a list of rows; each row is a list of values (any type). Convert each
  value to text with str().

Build a text table, and follow these rules EXACTLY:
1. Column width = the length of the longest text in that column (header included).
2. Each cell is left-justified (padded with spaces) to the column width.
3. Cells on a line are joined with " | " (space, pipe, space).
4. After joining, remove trailing whitespace from each line.
5. Line 2 is a separator: for each column, "-" repeated to the column width,
   joined with "-+-" (dash, plus, dash).
6. Output = header line, separator line, then one line per row, joined with "\n".
   No trailing newline.

Example:
    format_table(["name", "qty"], [["apple", 10], ["fig", 3]])
returns:
    name  | qty
    ------+----
    apple | 10
    fig   | 3

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
