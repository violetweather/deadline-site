# caesar_decode

Write a Python function:

    def decode(text: str, shift: int) -> str

The text was encoded with a Caesar cipher: each letter was moved FORWARD in the
alphabet by `shift` positions (wrapping around). Your function must decode it
(move letters back).

Rules:
- Preserve upper/lower case.
- Leave non-letter characters unchanged.
- shift can be 0, negative, or larger than 26.

Examples:
- decode("Khoor, Zruog!", 3) -> "Hello, World!"
- decode("abc", 0) -> "abc"

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
