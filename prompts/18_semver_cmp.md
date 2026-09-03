# semver_cmp

Write a Python function:

    def cmp_ver(a: str, b: str) -> int

Compare two semantic version strings. Return -1 if a < b, 0 if equal, 1 if a > b.

Format: MAJOR.MINOR.PATCH with an optional "-PRERELEASE" suffix
(e.g. "1.2.3", "1.0.0-alpha.1"). No build metadata. Input is always valid.

Precedence rules:
- Compare MAJOR, MINOR, PATCH numerically.
- A version WITH a prerelease is LOWER than the same version without one.
- Prerelease: split on "."; compare identifier by identifier:
  - two numeric identifiers compare as numbers
  - two alphanumeric identifiers compare as ASCII strings
  - a numeric identifier is LOWER than an alphanumeric one
  - if all shared identifiers are equal, the one with FEWER identifiers is lower.

Examples: cmp_ver("1.0.0-alpha", "1.0.0") -> -1, cmp_ver("1.0.0-beta.2", "1.0.0-beta.11") -> -1

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
