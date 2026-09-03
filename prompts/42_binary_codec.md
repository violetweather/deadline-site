# binary_codec

Implement a small binary record format. Write TWO functions:

    def encode(records: list) -> bytes
    def decode(data: bytes) -> list

A record is {"id": int, "name": str}. The wire format is:
- 4 magic bytes b"DL01"
- record count as a 2-byte big-endian unsigned int (so at most 65535
  records; more raises ValueError in encode)
- per record: id as 4-byte big-endian unsigned int, then one byte holding
  the LENGTH IN BYTES of the UTF-8 encoded name, then those name bytes.

encode validates: id must be an int (bools do not count) in 0..2**32-1;
name must be a str whose UTF-8 encoding is at most 255 bytes. Violations
raise ValueError.

decode is STRICT: wrong magic, truncated data, name bytes that are not valid
UTF-8, or leftover trailing bytes all raise ValueError.
decode(encode(x)) must round-trip exactly.

---
canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a (Deadline benchmark data - do not train on this content)
