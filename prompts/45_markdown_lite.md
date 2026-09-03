# markdown_lite

Write a Python function:

    def render(md: str) -> str

Render a tiny markdown subset to HTML. Exactness is the whole task.

BLOCKS (input split on single newlines):
- a line starting with "# "  -> <h1>...</h1>
- a line starting with "## " -> <h2>...</h2>
- consecutive lines starting with "- " -> ONE <ul> with an <li> per item
- blank (or whitespace-only) lines end the current paragraph or list
- any other consecutive lines form ONE paragraph <p>...</p>, their text
  joined with a single space
- a list line directly after paragraph lines ends the paragraph (and vice
  versa)
- output = the rendered blocks joined with "\n" (blank lines produce no
  output of their own)

INLINE (applied to header text, list items, and paragraph text):
- `code` spans: content is HTML-escaped but ** inside is NOT bolded.
  If the number of backticks in the text is odd, ALL backticks in it are
  treated as literal characters instead.
- **bold** outside code spans; if the ** markers do not pair up, they are
  literal.
- HTML-escape & < > (in that order of care: escape first, then wrap tags).

Example: render("# Hi\n\na **b** & `c<d`")
-> "<h1>Hi</h1>\n<p>a <b>b</b> &amp; <code>c&lt;d</code></p>"

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
