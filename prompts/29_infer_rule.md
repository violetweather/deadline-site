# infer_rule

Write a Python function:

    def transform(s: str) -> str

There is a hidden, deterministic rule. You must infer it from the examples
below and implement it EXACTLY. Hints, and they are the only hints:
the rule uses only the characters of s and their positions, and it is a
composition of two simple steps applied one after the other. Every example
below is exact and the hidden tests use inputs of the same kind.

    transform('') -> '|'
    transform('a') -> '|a'
    transform('b') -> 'b|'
    transform('ab') -> '|ba'
    transform('abc') -> 'c|ba'
    transform('bcd') -> 'bd|c'
    transform('bcdfg') -> 'bdg|fc'
    transform('xyz') -> 'xz|y'
    transform('hello') -> 'o|lehl'
    transform('queue') -> 'uuqee|'
    transform('rhythm') -> 'ryh|mth'
    transform('Deadline') -> '|eideDaln'
    transform('AEIOU') -> 'EAIU|O'
    transform('cab') -> 'b|ac'
    transform('zzzza') -> 'za|zzz'
    transform('abcdefgh') -> 'eg|hfdbac'
    transform('OK') -> '|KO'
    transform('stray') -> 'ry|ats'

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
