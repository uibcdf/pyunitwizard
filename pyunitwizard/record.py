"""QuantityRecord: PyUnitWizard's inert interchange form (provisional).

A quantity record carries values together with a verified description of their unit, so
that a number is never read in a unit it was not written in. It is a *form* like
``"string"``: it converts to and from every other form, and it does not compute. To
compute, convert it to ``pint``, ``openmm.unit``, ``astropy.units`` or ``unyt``.

Design, alternatives and measurements: uibcdf/pyunitwizard#83. Implementation issue:
uibcdf/pyunitwizard#82. The API is **provisional** until the 1.0 checklist promotes it
(``devguide/release_1.0.0_checklist.md``).

What a record guarantees:

- **The unit travels inside the same object as the values.** Its canonical name and its
  description in SI base units (factor, offset, exponents) are both recorded, and readers
  check that they agree.
- **A seal.** A blake2b digest covers the manifest and the values' bytes. Only this module
  produces it, so any change made elsewhere (a hand edit, a raw append, a renamed unit)
  fails on read.
- **A handshake.** Readers may declare the field, unit, dimensionality or kind they
  expect; a disagreement is an error.
- **No defaults.** A record without a manifest is refused; there is no fallback unit.

It is not a "passport" (see ``standards/PYUNITWIZARD_GUIDE.md``). It remembers nothing
about live objects and never lets a check be skipped; it is verified every time it is read.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import struct
from functools import lru_cache
from typing import Any, Dict, Mapping, Optional, Tuple

import numpy as np

from ._private.exceptions import RecordError

__all__ = ["FORMAT", "BUNDLE_FORMAT", "QuantityRecord", "QuantityRecordBundle", "RecordError"]

FORMAT = "qrec/0.3"
BUNDLE_FORMAT = "qrec-bundle/0.3"
#: Relative tolerance between a record's SI description and this reader's definition of the
#: same unit. Definitions differ across CODATA revisions (dalton: ~1.4e-9 between 2018 and
#: 2022) and libraries (UDUNITS' ``u`` differs from pint's dalton by ~7e-7). Distinct units
#: are never this close, so a larger disagreement means the unit is not what it claims.
REL_TOL = 1e-6
DTYPES = ("float64", "float32", "int64", "int32", "int16", "uint8", "uint16")
_SI_BASE = {
    "[length]": "m",
    "[mass]": "kg",
    "[time]": "s",
    "[current]": "A",
    "[temperature]": "K",
    "[substance]": "mol",
    "[luminosity]": "cd",
}


# --- canonical bytes ---------------------------------------------------------------------------


def _canonical(obj: Any) -> bytes:
    """Language-independent encoding of manifest data.

    JSON text is not canonical across languages (Python writes ``1e-06``, JavaScript
    ``0.000001``), so the digest is computed over this tagged little-endian encoding.
    Map keys are sorted by their UTF-8 bytes.
    """
    if obj is None:
        return b"n"
    if isinstance(obj, bool):
        return b"t" if obj else b"f"
    if isinstance(obj, int):
        return b"i" + struct.pack("<q", obj)
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            raise RecordError(reason="a manifest cannot hold a non-finite number")
        return b"d" + struct.pack("<d", obj)
    if isinstance(obj, str):
        data = obj.encode("utf-8")
        return b"s" + struct.pack("<I", len(data)) + data
    if isinstance(obj, (list, tuple)):
        return b"l" + struct.pack("<I", len(obj)) + b"".join(_canonical(item) for item in obj)
    if isinstance(obj, dict):
        items = sorted((str(key).encode("utf-8"), value) for key, value in obj.items())
        return (
            b"m"
            + struct.pack("<I", len(items))
            + b"".join(struct.pack("<I", len(key)) + key + _canonical(value) for key, value in items)
        )
    raise RecordError(reason=f"type {type(obj).__name__} cannot appear in a manifest")


def _little_endian(values: np.ndarray) -> memoryview:
    """C-order little-endian bytes, with every NaN written as the canonical quiet NaN."""
    dtype = values.dtype.newbyteorder("<")
    if values.dtype.kind == "f" and np.isnan(values).any():
        values = np.where(np.isnan(values), np.array(np.nan, dtype=dtype), values)
    if values.dtype != dtype or not values.flags.c_contiguous:
        values = np.ascontiguousarray(values, dtype=dtype)
    return memoryview(values).cast("B")


def _digest(*parts: Any) -> str:
    h = hashlib.blake2b(digest_size=16)
    for part in parts:
        h.update(part if isinstance(part, (bytes, memoryview)) else _canonical(part))
    return "blake2b-128:" + h.hexdigest()


def _seal(manifest: Dict[str, Any], values: np.ndarray) -> Tuple[list, str]:
    """Block digests and record digest. Only the codec may call this."""
    flat = np.asarray(values, dtype=np.dtype(manifest["dtype"])).reshape(-1)
    block_digests, start = [], 0
    for index, size in enumerate(manifest["blocks"]):
        block = flat[start : start + size]
        block_digests.append(_digest({"block": index, "dtype": manifest["dtype"]}, _little_endian(block)))
        start += size
    return block_digests, _digest(manifest, *[d.encode("ascii") for d in block_digests])


# --- unit description --------------------------------------------------------------------------


def _registry():
    from .forms.api_pint import ureg

    return ureg


def _canonical_name(unit: Any) -> str:
    """PyUnitWizard's canonical spelling: pint's default long form, whatever the display
    format a user configured on the registry."""
    return format(unit, "D")


@lru_cache(maxsize=None)
def _describe(unit: str) -> str:
    ureg = _registry()
    one = ureg.Quantity(1.0, unit)
    zero = ureg.Quantity(0.0, unit)
    base_one, base_zero = one.to_base_units(), zero.to_base_units()
    exponents: Dict[str, Any] = {}
    for dimension, exponent in dict(one.dimensionality).items():
        if not exponent:
            continue
        if dimension not in _SI_BASE:
            raise RecordError(reason=f"unit {unit!r} has a dimension outside the SI base: {dimension}")
        exponents[_SI_BASE[dimension]] = int(exponent) if float(exponent).is_integer() else float(exponent)
    offset = float(base_zero.magnitude)
    return json.dumps(
        {
            "unit": _canonical_name(one.units),
            "si": {
                "factor": float(base_one.magnitude) - offset,
                "offset": offset,
                "exponents": dict(sorted(exponents.items())),
            },
        }
    )


def _descriptor(unit: str) -> Dict[str, Any]:
    """A fresh description every call: a record must never share state with the cache
    that checks it."""
    return json.loads(_describe(unit))


def _cross_check(description: Mapping[str, Any], field: Optional[str]) -> None:
    """The unit's name and its SI description must tell the same story."""
    try:
        reference = _descriptor(description["unit"])
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason=f"unit {description['unit']!r} is not known to this reader", field=field) from exc
    if reference["unit"] != description["unit"]:
        raise RecordError(reason=f"unit {description['unit']!r} is not in canonical spelling", field=field)
    si, ref = description["si"], reference["si"]
    if si["exponents"] != ref["exponents"]:
        raise RecordError(reason=f"unit {description['unit']!r} disagrees with its SI dimensions", field=field)
    for key in ("factor", "offset"):
        a, b = si[key], ref[key]
        if not (a == b == 0) and abs(a - b) > REL_TOL * max(abs(a), abs(b)):
            raise RecordError(reason=f"unit {description['unit']!r} disagrees with its SI {key}", field=field)


# --- values ----------------------------------------------------------------------------------------


def _normalize_dtype(values: np.ndarray) -> np.ndarray:
    if values.dtype.name in DTYPES:
        return values
    if values.dtype.kind == "f":
        return values.astype(np.float64)
    if values.dtype.kind == "i" or (values.dtype.kind == "u" and values.dtype.itemsize <= 4):
        return values.astype(np.int64)
    raise RecordError(reason=f"values of dtype {values.dtype.name} cannot be recorded")


def _to_pint(quantity: Any, unit: Optional[str] = None):
    from .api.conversion import convert
    from .api.introspection import is_quantity

    if isinstance(quantity, QuantityRecord):
        return quantity.to_quantity(form="pint", unit=unit)
    if not is_quantity(quantity):
        raise RecordError(reason="a record is built from a quantity, not from a bare value")
    return convert(quantity, to_form="pint", to_unit=unit)


def _decode(payload: Any, manifest: Mapping[str, Any], field: Optional[str]) -> np.ndarray:
    dtype = np.dtype(manifest["dtype"]).newbyteorder("<")
    try:
        if isinstance(payload, dict):
            values = np.frombuffer(base64.b64decode(payload["base64"], validate=True), dtype=dtype)
        else:
            values = np.asarray(payload, dtype=dtype)
        return values.reshape(manifest["shape"]).astype(dtype.newbyteorder("="), copy=True)
    except Exception as exc:
        raise RecordError(reason="values do not match the manifest's dtype and shape", field=field) from exc


def _encode(values: np.ndarray, encoding: str, field: Optional[str]) -> Any:
    if encoding == "base64":
        return {"base64": base64.b64encode(_little_endian(values)).decode("ascii")}
    if encoding != "json":
        raise RecordError(reason=f"unknown encoding {encoding!r}; use 'json' or 'base64'", field=field)
    if values.dtype.kind == "f" and not np.all(np.isfinite(values)):
        raise RecordError(
            reason="JSON has no NaN or infinity; use encoding='base64' for non-finite values", field=field
        )
    return values.tolist()


# --- QuantityRecord ----------------------------------------------------------------------------------


class QuantityRecord:
    """Values plus a verified description of their unit. Inert: it does not compute.

    Build one with :meth:`from_quantity` (or ``puw.convert(q, to_form="record")``), store
    it with :meth:`to_dict`, read it back with :meth:`from_dict`, and get a computing
    quantity with :meth:`to_quantity`.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> from pyunitwizard.record import QuantityRecord
    >>> record = QuantityRecord.from_quantity(puw.quantity(3.0, "nM"), field="ic50")
    >>> data = record.to_dict()                      # JSON-ready, sealed
    >>> q = QuantityRecord.from_dict(data).to_quantity(field="ic50", unit="uM")
    """

    __slots__ = ("_manifest", "_values", "_block_digests", "_digest")

    def __init__(self) -> None:  # pragma: no cover - construction goes through classmethods
        raise TypeError("build a QuantityRecord with from_quantity() or from_dict()")

    @classmethod
    def _new(cls, manifest, values, block_digests, digest) -> "QuantityRecord":
        record = object.__new__(cls)
        values = np.array(values, copy=True)
        values.setflags(write=False)
        record._manifest = manifest
        record._values = values
        record._block_digests = list(block_digests)
        record._digest = digest
        return record

    @classmethod
    def from_quantity(
        cls,
        quantity: Any,
        *,
        field: Optional[str] = None,
        unit: Optional[str] = None,
        kind: Optional[str] = None,
    ) -> "QuantityRecord":
        """Seal a quantity. The value and its unit are taken from the same object.

        Parameters
        ----------
        quantity : quantity in any PyUnitWizard form
            The quantity to record. Bare numbers are refused.
        field : str, optional
            The name the values are bound to. A reader that declares a field refuses a
            record bound to another one, or to none.
        unit : str, optional
            The negotiated unit to record in. Defaults to the quantity's own unit.
        kind : str, optional
            A quantity-kind identifier (a QUDT or OBO UO IRI, for instance). It tells apart
            units with equal SI dimensions, such as hertz and becquerel.

        Returns
        -------
        QuantityRecord

        Raises
        ------
        RecordError
            If ``quantity`` is not a quantity, or its values cannot be recorded.
        """
        q = _to_pint(quantity, unit)
        values = _normalize_dtype(np.asarray(q.magnitude))
        manifest: Dict[str, Any] = {"format": FORMAT, "field": field, **_descriptor(_canonical_name(q.units))}
        if kind is not None:
            manifest["kind"] = str(kind)
        manifest.update({"dtype": values.dtype.name, "shape": list(values.shape), "blocks": [int(values.size)]})
        block_digests, digest = _seal(manifest, values)
        return cls._new(manifest, values, block_digests, digest)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "QuantityRecord":
        """Read a stored record, refusing it unless every check passes.

        Raises
        ------
        RecordError
            If the manifest is missing or malformed, the seal does not verify, or the unit's
            name and SI description disagree.
        """
        if not isinstance(data, Mapping) or not isinstance(data.get("manifest"), Mapping):
            raise RecordError(reason="no manifest; there is no default unit")
        manifest = copy.deepcopy(dict(data["manifest"]))
        field = manifest.get("field")
        if manifest.get("format") != FORMAT:
            raise RecordError(reason=f"format {manifest.get('format')!r} is not {FORMAT!r}", field=field)
        for key in ("unit", "si", "dtype", "shape", "blocks"):
            if key not in manifest:
                raise RecordError(reason=f"the manifest has no {key!r}", field=field)
        if manifest["dtype"] not in DTYPES:
            raise RecordError(reason=f"dtype {manifest['dtype']!r} is not allowed", field=field)
        values = _decode(data.get("values"), manifest, field)
        if sum(manifest["blocks"]) != values.size or len(data.get("block_digests", [])) != len(manifest["blocks"]):
            raise RecordError(reason="the blocks do not cover the values", field=field)
        block_digests, digest = _seal(manifest, values)
        if list(data.get("block_digests", [])) != block_digests:
            raise RecordError(reason="the values were changed outside the codec", field=field)
        if data.get("digest") != digest:
            raise RecordError(reason="the manifest was changed outside the codec", field=field)
        _cross_check(manifest, field)
        return cls._new(manifest, values, block_digests, digest)

    def to_dict(self, *, encoding: str = "json") -> Dict[str, Any]:
        """The sealed, JSON-ready representation.

        Parameters
        ----------
        encoding : {"json", "base64"}
            ``"json"`` writes readable lists and refuses non-finite values, which JSON
            cannot hold. ``"base64"`` writes the little-endian bytes (about 1.33 times their
            raw size) and holds any value exactly.
        """
        return {
            "manifest": copy.deepcopy(self._manifest),
            "values": _encode(self._values, encoding, self.field),
            "block_digests": list(self._block_digests),
            "digest": self._digest,
        }

    def to_quantity(
        self,
        *,
        field: Optional[str] = None,
        unit: Optional[str] = None,
        dimensionality: Optional[Dict[str, int]] = None,
        kind: Optional[str] = None,
        form: Optional[str] = None,
    ):
        """A computing quantity, after the reader's handshake.

        Parameters
        ----------
        field : str, optional
            The field the reader expects. A record bound to another field, or to none, is
            refused.
        unit : str, optional
            Convert to this unit. A unit of other dimensions is refused.
        dimensionality : dict, optional
            Expected dimensionality in PyUnitWizard notation, e.g. ``{"[L]": 1}``.
        kind : str, optional
            The quantity kind the reader expects.
        form : str, optional
            The form to return. Defaults to the session's default form, or ``"pint"``.

        Raises
        ------
        RecordError
            If any expectation is not met.
        """
        from . import kernel
        from .api.conversion import convert
        from .api.validation import check

        if field is not None and self.field != field:
            raise RecordError(reason=f"the record belongs to {self.field!r}, not {field!r}", field=field)
        if kind is not None and self.kind != kind:
            raise RecordError(reason=f"expected kind {kind!r}, the record holds {self.kind!r}", field=self.field)
        q = _registry().Quantity(np.array(self._values, copy=True), self.unit)
        if unit is not None:
            target = _descriptor(str(unit))
            if target["si"]["exponents"] != self.si["exponents"]:
                raise RecordError(reason=f"{self.unit!r} cannot be read as {unit!r}", field=self.field)
            if target["unit"] != self.unit:
                q = q.to(target["unit"])
        if dimensionality is not None and not check(q, dimensionality=dimensionality):
            raise RecordError(
                reason=f"expected dimensionality {dimensionality}, the record holds {self.unit!r}", field=self.field
            )
        target_form = form or kernel.default_form or "pint"
        return q if target_form == "pint" else convert(q, to_form=target_form)

    # --- read-only views -------------------------------------------------------------

    @property
    def field(self) -> Optional[str]:
        return self._manifest.get("field")

    @property
    def unit(self) -> str:
        return self._manifest["unit"]

    @property
    def si(self) -> Dict[str, Any]:
        return copy.deepcopy(self._manifest["si"])

    @property
    def kind(self) -> Optional[str]:
        return self._manifest.get("kind")

    @property
    def values(self) -> np.ndarray:
        """The recorded values, read-only: they cannot change behind the seal."""
        return self._values

    @property
    def digest(self) -> str:
        return self._digest

    def __repr__(self) -> str:
        return (
            f"QuantityRecord(field={self.field!r}, unit={self.unit!r}, "
            f"shape={tuple(self._values.shape)}, dtype={self._values.dtype.name})"
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, QuantityRecord) and other._digest == self._digest

    def __hash__(self) -> int:
        return hash(self._digest)


# --- bundles ---------------------------------------------------------------------------------------


class QuantityRecordBundle:
    """Many small quantities under one seal, for documents such as a card.

    A separate record per scalar costs about 350 bytes; a bundle about half, with a single
    digest over every entry, its unit description and its values.
    """

    __slots__ = ("_entries", "_digest")

    def __init__(self) -> None:  # pragma: no cover
        raise TypeError("build a QuantityRecordBundle with from_quantities() or from_dict()")

    @classmethod
    def _new(cls, entries, digest) -> "QuantityRecordBundle":
        bundle = object.__new__(cls)
        bundle._entries = entries
        bundle._digest = digest
        return bundle

    @staticmethod
    def _parts(entries: Mapping[str, Tuple[Dict[str, Any], np.ndarray]]) -> list:
        parts: list = [{"format": BUNDLE_FORMAT}]
        for name in sorted(entries):
            description, values = entries[name]
            parts += [name, description, _little_endian(values)]
        return parts

    @classmethod
    def from_quantities(
        cls, quantities: Mapping[str, Any], *, kinds: Optional[Mapping[str, str]] = None
    ) -> "QuantityRecordBundle":
        """Seal a mapping of field names to quantities (any PyUnitWizard form)."""
        entries = {}
        for name, quantity in quantities.items():
            q = _to_pint(quantity)
            values = _normalize_dtype(np.asarray(q.magnitude))
            description = _descriptor(_canonical_name(q.units))
            if kinds and name in kinds:
                description["kind"] = str(kinds[name])
            description.update({"dtype": values.dtype.name, "shape": list(values.shape)})
            values = np.array(values, copy=True)
            values.setflags(write=False)
            entries[str(name)] = (description, values)
        return cls._new(entries, _digest(*cls._parts(entries)))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "QuantityRecordBundle":
        """Read a stored bundle, refusing it unless the seal and every unit check pass."""
        if not isinstance(data, Mapping) or data.get("format") != BUNDLE_FORMAT:
            raise RecordError(reason=f"not a {BUNDLE_FORMAT!r} bundle")
        entries = {}
        for name, stored in dict(data.get("entries") or {}).items():
            description = {k: copy.deepcopy(v) for k, v in stored.items() if k != "values"}
            for key in ("unit", "si", "dtype", "shape"):
                if key not in description:
                    raise RecordError(reason=f"the entry has no {key!r}", field=name)
            if description["dtype"] not in DTYPES:
                raise RecordError(reason=f"dtype {description['dtype']!r} is not allowed", field=name)
            values = _decode(stored.get("values"), description, name)
            values.setflags(write=False)
            entries[name] = (description, values)
        if data.get("digest") != _digest(*cls._parts(entries)):
            raise RecordError(reason="the bundle was changed outside the codec")
        for name, (description, _) in entries.items():
            _cross_check(description, name)
        return cls._new(entries, data["digest"])

    def to_dict(self) -> Dict[str, Any]:
        """The sealed, JSON-ready representation (strict JSON; non-finite values refused)."""
        entries = {}
        for name in sorted(self._entries):
            description, values = self._entries[name]
            entries[name] = {**copy.deepcopy(description), "values": _encode(values, "json", name)}
        return {"format": BUNDLE_FORMAT, "entries": entries, "digest": self._digest}

    @property
    def fields(self) -> list:
        return sorted(self._entries)

    def to_quantities(
        self, *, expected: Optional[Mapping[str, Optional[Dict[str, int]]]] = None, form: Optional[str] = None
    ) -> Dict[str, Any]:
        """Computing quantities, after the handshake.

        Parameters
        ----------
        expected : dict, optional
            Every field the reader expects, mapped to its expected dimensionality (or
            ``None``). A bundle holding other fields, or missing one, is refused.
        form : str, optional
            The form to return. Defaults to the session's default form, or ``"pint"``.
        """
        from . import kernel
        from .api.conversion import convert
        from .api.validation import check

        if expected is not None and set(expected) != set(self._entries):
            raise RecordError(reason=f"the bundle holds {self.fields}, expected {sorted(expected)}")
        target_form = form or kernel.default_form or "pint"
        out = {}
        for name, (description, values) in self._entries.items():
            q = _registry().Quantity(np.array(values, copy=True), description["unit"])
            wanted = (expected or {}).get(name)
            if wanted is not None and not check(q, dimensionality=wanted):
                raise RecordError(
                    reason=f"expected dimensionality {wanted}, the entry holds {description['unit']!r}", field=name
                )
            out[name] = q if target_form == "pint" else convert(q, to_form=target_form)
        return out

    def __repr__(self) -> str:
        return f"QuantityRecordBundle(fields={self.fields})"


# --- the "record" form inside convert() -------------------------------------------------------------


def _convert_with_records(obj, *, form_in, to_unit, to_form, parser, to_type):
    """convert() delegates here whenever the source or the target form is "record"."""
    from ._private.exceptions import ArgumentError
    from .api.conversion import convert

    if to_type not in ("quantity", "unit", "value"):
        raise ArgumentError(argument="to_type")
    unit_name = None
    if to_unit is not None:
        unit_name = (
            to_unit if isinstance(to_unit, str) else _canonical_name(convert(to_unit, to_form="pint", to_type="unit"))
        )
    if form_in == "record":
        q = obj.to_quantity(form="pint", unit=unit_name)
        field, kind = obj.field, obj.kind
    else:
        q = convert(obj, to_form="pint", to_unit=unit_name, parser=parser)
        field = kind = None
    if to_form != "record":
        return convert(q, to_form=to_form, to_type=to_type, parser=parser)
    if to_type == "unit":
        return _canonical_name(q.units)
    if to_type == "value":
        value = np.array(q.magnitude, copy=True)
        return value.item() if value.ndim == 0 else value
    return QuantityRecord.from_quantity(q, field=field, kind=kind)
