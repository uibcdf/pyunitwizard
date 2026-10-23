"""Implementation of the provisional tagged layout of QuantityRecord.

Public entry points live on QuantityRecord. Existing qrec/0.3 bytes stay unchanged.
"""

import copy

import numpy as np

from ._private.exceptions import RecordError


def seal(cls, manifest, values, codes):
    from .record import _digest, _little_endian

    codes = np.asarray(codes, dtype=np.uint16)
    block = _digest(_little_endian(values), _little_endian(codes))
    record = cls._new(copy.deepcopy(manifest), values, [block], _digest(manifest, block.encode("ascii")))
    record._codes = np.frombuffer(codes.tobytes(order="C"), dtype=np.uint16).reshape(codes.shape)
    return record


def build(cls, quantities, *, field, kinds):
    from .record import TAGGED_FORMAT, _canonical_name, _descriptor, _normalize_dtype, _to_pint

    sources = list(quantities)
    if not sources:
        raise RecordError(reason="a tagged collection requires at least one source quantity")
    kinds = [None] * len(sources) if kinds is None else list(kinds)
    if len(kinds) != len(sources) or any(k is not None and not isinstance(k, str) for k in kinds):
        raise RecordError(reason="one explicit string kind or None is required per source")
    values, codes, descriptors = [], [], []
    for source, kind in zip(sources, kinds):
        q = _to_pint(source)
        descriptor = _descriptor(_canonical_name(q.units))
        if kind is not None:
            descriptor["kind"] = kind
        if descriptor not in descriptors:
            descriptors.append(descriptor)
        values.append(_normalize_dtype(np.asarray(q.magnitude)))
        codes.append(descriptors.index(descriptor))
    if len(descriptors) > 65536 or any(v.shape != values[0].shape for v in values):
        raise RecordError(reason="tagged sources require equal shapes and at most 65536 descriptors")
    sources = values
    values = _normalize_dtype(np.stack(sources))
    for index, source in enumerate(sources):
        with np.errstate(invalid="ignore", over="ignore"):
            recovered = values[index].astype(source.dtype)
        if not np.array_equal(recovered, source, equal_nan=True):
            raise RecordError(reason="common tagged dtype would lose source precision")
    codes = np.broadcast_to(np.array(codes, dtype=np.uint16).reshape((-1,) + (1,) * (values.ndim - 1)), values.shape)
    manifest = {
        "format": TAGGED_FORMAT,
        "layout": "tagged",
        "field": field,
        "dtype": values.dtype.name,
        "shape": list(values.shape),
        "descriptors": descriptors,
    }
    return seal(cls, manifest, values, codes)


def restore(cls, data):
    from .record import DTYPES, _cross_check, _decode

    try:
        manifest = copy.deepcopy(data["manifest"])
        descriptors = manifest["descriptors"]
        if not isinstance(manifest["shape"], list) or any(type(n) is not int or n < 0 for n in manifest["shape"]):
            raise ValueError("tagged shape must contain explicit nonnegative integer sizes")
        if (
            manifest["layout"] != "tagged"
            or manifest["dtype"] not in DTYPES
            or not isinstance(descriptors, list)
            or not 0 < len(descriptors) <= 65536
        ):
            raise ValueError("tagged manifest")
        values = _decode(data["values"], manifest, manifest.get("field"))
        raw_codes = np.asarray(data["codes"])
        if not raw_codes.size and not values.size:
            raw_codes = raw_codes.reshape(values.shape).astype(np.uint16)
        if (
            raw_codes.shape != values.shape
            or (raw_codes.size and raw_codes.dtype.kind not in "iu")
            or np.any(raw_codes < 0)
            or np.any(raw_codes >= len(descriptors))
        ):
            raise ValueError("descriptor codes")
        for descriptor in descriptors:
            _cross_check(descriptor, manifest.get("field"))
            if descriptor.get("kind") is not None and not isinstance(descriptor["kind"], str):
                raise ValueError("descriptor kind")
        record = seal(cls, manifest, values, raw_codes)
        if record.digest != data["digest"] or record._block_digests != data["block_digests"]:
            raise ValueError("tagged seal")
        return record
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason=f"invalid tagged record: {exc}") from exc


def split(record):
    from .record import QuantityRecord, _registry

    if record.layout != "tagged":
        raise RecordError(reason="split requires a tagged record")
    return {
        index: QuantityRecord.from_quantity(
            _registry().Quantity(record.values[record.codes == index], descriptor["unit"]),
            field=record.field,
            kind=descriptor.get("kind"),
        )
        for index, descriptor in enumerate(record.descriptors)
    }


def to_quantity(record, *, field, unit, dimensionality, kind, form):
    from .api.conversion import convert
    from .record import _registry

    if unit is None:
        raise RecordError(reason="tagged computation requires an explicit unit or split()", field=record.field)
    descriptors = record.descriptors
    if len({d.get("kind") for d in descriptors}) != 1:
        raise RecordError(reason="incompatible quantity kinds require split()", field=record.field)
    try:
        groups = split(record)
        converted = {
            i: group.to_quantity(field=field, unit=unit, dimensionality=dimensionality, kind=kind, form="pint")
            for i, group in groups.items()
        }
        dtype = np.result_type(*[q.magnitude.dtype for q in converted.values()])
        values = np.empty(record.values.shape, dtype=dtype)
        for index, q in converted.items():
            values[record.codes == index] = q.magnitude
        q = _registry().Quantity(values, unit)
        return q if form == "pint" else convert(q, to_form=form)
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason=f"tagged values cannot share target unit {unit!r}", field=record.field) from exc
