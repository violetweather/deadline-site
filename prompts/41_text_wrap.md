# text_wrap

Write a Python function:

    def wrap(text: str, width: int) -> list

Greedy word-wrap. Rules:
- width < 1 raises ValueError.
- Paragraphs are separated by exactly "\n\n" in the input; in the output,
  paragraphs are separated by one empty string "".
- Within a paragraph, words are whitespace-separated tokens (all other
  whitespace collapses). Fill lines greedily: add the next word if the line
  plus one space plus the word fits in `width`.
- A word LONGER than width is hard-broken into width-sized chunks first;
  the chunks then flow like ordinary words.
- No trailing spaces; empty paragraphs produce no lines.

Example: wrap("aa bb cc", 5) -> ["aa bb", "cc"]

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
