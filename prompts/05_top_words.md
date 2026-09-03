# top_words

Write a Python function:

    def top_words(text: str, k: int) -> list

Steps:
1. Lowercase the text.
2. Words are maximal runs of ASCII letters (a-z). Every other character separates words.
3. Count how often each word appears.
4. Sort by count (highest first). Break ties alphabetically (a before z).
5. Return the first k words as a list of strings. If there are fewer than k
   unique words, return all of them.

Examples:
- top_words("The cat and the hat", 2) -> ["the", "and"]
- top_words("a b b c c c", 2) -> ["c", "b"]

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
