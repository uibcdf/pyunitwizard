"""Provisional verified HDF5 snapshot binding (qrec-hdf5/0.1).

One group contains values and their authoritative sealed record metadata. CF
presentation attributes are separately bound to that record; neither root-unit
fallbacks nor raw append semantics are supported. Reads verify the whole array.
"""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict, Optional

import numpy as np

from pyunitwizard._private.exceptions import RecordError
from pyunitwizard.record import QuantityRecord, _digest

__all__ = ["FORMAT", "read", "write"]
FORMAT = "qrec-hdf5/0.1"


def _provider():
    from depdigest import is_installed

    if not is_installed("h5py"):
        raise ModuleNotFoundError("Install optional HDF5 tools with conda install -c conda-forge h5py=3.16.0")
    import h5py

    return h5py


def _text(value):
    return value.decode("utf-8") if isinstance(value, bytes) else value


def _unique_keys(pairs):
    node = {}
    for key, value in pairs:
        if key in node:
            raise RecordError(reason="duplicate keys in HDF5 record metadata")
        node[key] = value
    return node


def write(
    parent: Any,
    name: str,
    record: QuantityRecord,
    *,
    cf_unit: str,
    units_metadata: Optional[str] = None,
) -> Any:
    """Create one verified snapshot group without overwriting existing data.

    Parameters
    ----------
    parent : h5py.File or h5py.Group
        Writable destination. The caller owns opening, closing and flushing it.
    name : str
        New direct child name, without path separators.
    record : QuantityRecord
        Immutable sealed source snapshot. Values, dtype and qrec seal are kept.
    cf_unit : str
        Explicit negotiated CF label checked against the record's actual unit.
    units_metadata : str, optional
        Required explicit on-scale/difference semantics for temperature.

    Returns
    -------
    h5py.Group
        Group containing a numeric values dataset and authoritative metadata.
        Validation occurs before staging; a write error removes the staged group.

    Raises
    ------
    RecordError
        For invalid inputs, conflicting CF labels, existing names or I/O failure.
    ModuleNotFoundError
        If h5py or cf-units is unavailable.

    Examples
    --------
    >>> group = write(file, 'coordinates', record, cf_unit='nm')
    """
    provider = _provider()
    if not isinstance(parent, provider.Group) or not isinstance(record, QuantityRecord):
        raise RecordError(reason="HDF5 write requires a group and an immutable QuantityRecord")
    if not isinstance(name, str) or not name or name in {".", ".."} or "/" in name or "\x00" in name:
        raise RecordError(reason="HDF5 record name must be a nonempty direct child")
    if name in parent:
        raise RecordError(reason="HDF5 write never overwrites an existing child", field=record.field)
    from pyunitwizard.dialects.cf import validate_unit

    validate_unit(record.unit, cf_unit, units_metadata=units_metadata)
    # Base64 handles NaN/Inf exactly; its bytes stay in the dataset rather than JSON.
    envelope = record.to_dict(encoding="base64")
    envelope.pop("values")
    node = {"format": FORMAT, "record": envelope, "units": cf_unit, "units_metadata": units_metadata}
    node["digest"] = _digest(node)
    encoded = json.dumps(node, sort_keys=True, separators=(",", ":"), allow_nan=False)
    staging = ".pyunitwizard-" + uuid.uuid4().hex
    try:
        group = parent.create_group(staging)
        group.create_dataset("values", data=record.values)
        group.attrs["units"] = cf_unit
        if units_metadata is not None:
            group.attrs["units_metadata"] = units_metadata
        group.attrs["pyunitwizard"] = encoded
        parent.move(staging, name)
        return parent[name]
    except Exception as exc:
        if staging in parent:
            del parent[staging]
        raise RecordError(
            reason="HDF5 snapshot creation failed; no staged snapshot retained", field=record.field
        ) from exc


def read(
    group: Any,
    *,
    field: Optional[str] = None,
    unit: Optional[str] = None,
    dimensionality: Optional[Dict[str, int]] = None,
    kind: Optional[str] = None,
    units_metadata: Optional[str] = None,
) -> QuantityRecord:
    """Verify a complete HDF5 snapshot and its reader expectations.

    Parameters
    ----------
    group : h5py.Group
        Group previously created by write; no legacy unit fallback is permitted.
    field : str, optional
        Expected logical field; paths alone do not establish field identity.
    unit : str, optional
        Required compatible computing unit. The returned record retains its
        original unit and seal; call to_quantity to convert it.
    dimensionality : dict, optional
        Expected dimensions in PyUnitWizard notation.
    kind : str, optional
        Expected quantity kind identifier.
    units_metadata : str, optional
        Required reader expectation for temperature: on_scale or difference.
        A missing or different expectation is refused. Returned records retain
        their original computing-unit contract; this expectation belongs to
        the binding and is not silently added to qrec/0.3.

    Returns
    -------
    QuantityRecord
        Detached immutable snapshot after full value, manifest and CF checks.
        Every read materializes and verifies the entire dataset.

    Raises
    ------
    RecordError
        For missing/conflicting metadata, edited values/dtype/shape, raw appends,
        unsupported binding versions or reader expectation failures.
    ModuleNotFoundError
        If an optional provider is unavailable.

    Examples
    --------
    >>> record = read(file['coordinates'], field='coordinates', unit='nanometer')
    """
    provider = _provider()
    if not isinstance(group, provider.Group):
        raise RecordError(reason="HDF5 read requires a verified snapshot group")
    try:
        node = json.loads(_text(group.attrs["pyunitwizard"]), object_pairs_hook=_unique_keys)
        if not isinstance(node, dict) or set(node) != {"format", "record", "units", "units_metadata", "digest"}:
            raise RecordError(reason="HDF5 snapshot has an invalid binding envelope")
        digest = node.pop("digest")
        if node["format"] != FORMAT or _digest(node) != digest:
            raise RecordError(reason="HDF5 binding metadata was changed outside the codec")
        metadata = node["units_metadata"]
        if metadata != units_metadata:
            raise RecordError(reason="reader temperature semantics disagree with the HDF5 binding")
        attributes = {"units", "pyunitwizard"} | ({"units_metadata"} if metadata is not None else set())
        if set(group.attrs) != attributes or _text(group.attrs["units"]) != node["units"]:
            raise RecordError(reason="HDF5 CF attributes are missing or conflict with the binding seal")
        if metadata is not None and _text(group.attrs["units_metadata"]) != metadata:
            raise RecordError(reason="HDF5 temperature semantics disagree with the binding seal")
        if set(group) != {"values"}:
            raise RecordError(reason="HDF5 snapshot must contain exactly one values dataset")
        dataset = group["values"]
        if not isinstance(dataset, provider.Dataset) or len(dataset.attrs):
            raise RecordError(reason="HDF5 values have a conflicting secondary declaration")
        envelope = node["record"]
        manifest = envelope["manifest"]
        if dataset.dtype.name != manifest["dtype"] or list(dataset.shape) != manifest["shape"]:
            raise RecordError(reason="HDF5 values dtype or shape was changed outside the codec")
        values = dataset[()]
        # Delegate byte verification to the existing codec; no storage-local seal
        # algorithm or permissive fallback reinterprets the original record.
        envelope["values"] = np.asarray(values)
        record = QuantityRecord.from_dict(envelope)
        from pyunitwizard.dialects.cf import parse_quantity, validate_unit

        validate_unit(record.unit, node["units"], units_metadata=metadata)
        if unit is not None:
            parse_quantity(0.0, node["units"], unit=unit, units_metadata=metadata, form="pint")
        record.to_quantity(field=field, unit=unit, dimensionality=dimensionality, kind=kind, form="pint")
        return record
    except (ModuleNotFoundError, RecordError):
        raise
    except Exception as exc:
        raise RecordError(reason="HDF5 snapshot is missing or has malformed metadata or values", field=field) from exc
