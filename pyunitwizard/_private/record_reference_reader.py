"""Reference reader for quantity records, using only the Python standard library.

It exists to show that the format needs no PyUnitWizard, pint or numpy to be read and
verified, and to serve as a template for readers in other languages: every byte it hashes
is defined by the format, not by a library. It reads JSON-encoded and base64 records and
returns SI values after checking the seal and the expected SI dimensions.
"""

import base64
import hashlib
import struct

FORMAT = "qrec/0.3"
_STRUCT = {"float64": "d", "float32": "f", "int64": "q", "int32": "i", "int16": "h", "uint8": "B", "uint16": "H"}


def canonical(obj):
    """Tagged little-endian encoding of manifest data (see pyunitwizard.record)."""
    if obj is None:
        return b"n"
    if isinstance(obj, bool):
        return b"t" if obj else b"f"
    if isinstance(obj, int):
        return b"i" + struct.pack("<q", obj)
    if isinstance(obj, float):
        return b"d" + struct.pack("<d", obj)
    if isinstance(obj, str):
        data = obj.encode("utf-8")
        return b"s" + struct.pack("<I", len(data)) + data
    if isinstance(obj, list):
        return b"l" + struct.pack("<I", len(obj)) + b"".join(canonical(item) for item in obj)
    items = sorted((key.encode("utf-8"), value) for key, value in obj.items())
    return (
        b"m"
        + struct.pack("<I", len(items))
        + b"".join(struct.pack("<I", len(key)) + key + canonical(value) for key, value in items)
    )


def _flatten(values):
    if isinstance(values, list):
        return [item for value in values for item in _flatten(value)]
    return [values]


def _blake2b(*parts):
    h = hashlib.blake2b(digest_size=16)
    for part in parts:
        h.update(part)
    return "blake2b-128:" + h.hexdigest()


def read_si(record, field, exponents):
    """Verify a record and return its values in SI base units.

    Raises ``ValueError`` if the format, field, seal or SI dimensions are not as expected.
    """
    manifest = record["manifest"]
    if manifest.get("format") != FORMAT or manifest.get("field") != field:
        raise ValueError("wrong format or field")
    code = _STRUCT[manifest["dtype"]]
    payload = record["values"]
    if isinstance(payload, dict):
        raw = base64.b64decode(payload["base64"])
        values = list(struct.unpack("<%d%s" % (len(raw) // struct.calcsize(code), code), raw))
    else:
        values = _flatten(payload)
    nan = struct.unpack("<d", struct.pack("<Q", 0x7FF8000000000000))[0]
    start = 0
    for index, (size, stored) in enumerate(zip(manifest["blocks"], record["block_digests"])):
        block = [nan if v != v else v for v in values[start : start + size]]
        start += size
        packed = struct.pack("<%d%s" % (size, code), *block)
        if _blake2b(canonical({"block": index, "dtype": manifest["dtype"]}), packed) != stored:
            raise ValueError("block %d was changed outside the codec" % index)
    if start != len(values):
        raise ValueError("the blocks do not cover the values")
    top = _blake2b(canonical(manifest), *[d.encode("ascii") for d in record["block_digests"]])
    if top != record["digest"]:
        raise ValueError("the manifest was changed outside the codec")
    si = manifest["si"]
    if si["exponents"] != exponents:
        raise ValueError("expected SI dimensions %r, got %r" % (exponents, si["exponents"]))
    return [value * si["factor"] + si["offset"] for value in values]
