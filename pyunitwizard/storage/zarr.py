"""Provisional qrec-zarr/0.1 snapshots with verified first-axis chunk reads.

The caller owns the Zarr store and concurrency. Publication requires a new group;
there is no append, overwrite or concurrent-writer/crash-transaction guarantee.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

import numpy as np

from pyunitwizard.record import QuantityRecord, RecordError, metadata_digest

FORMAT = "qrec-zarr/0.1"


def _provider():
    from depdigest import is_installed

    if not is_installed("zarr"):
        raise ModuleNotFoundError("Install optional Zarr tools with conda install -c conda-forge zarr=3.1.6")
    import zarr

    return zarr


def _record(values, metadata):
    from pyunitwizard.forms.api_pint import ureg

    manifest = metadata["manifest"]
    return QuantityRecord.from_quantity(
        ureg.Quantity(values, manifest["unit"]), field=manifest.get("field"), kind=manifest.get("kind")
    )


def write(parent: Any, name: str, record: QuantityRecord, *, chunk_rows: int = 64) -> Any:
    """Write a new verified homogeneous snapshot with first-axis chunking.

    Parameters
    ----------
    parent : zarr.Group
        Caller-owned writable group (Zarr format 3).
    name : str
        New direct child name; existing data is never overwritten.
    record : QuantityRecord
        Homogeneous sealed source. All values remain in their recorded unit.
    chunk_rows : int
        Positive number of rows per physical and verification chunk.

    Returns
    -------
    zarr.Group
        Complete group with one values array and authoritative sealed metadata.

    Raises
    ------
    RecordError
        For invalid inputs, existing names, tagged layouts or a write failure.
    ModuleNotFoundError
        If the optional Zarr provider is absent.

    Examples
    --------
    >>> group = write(root, 'coordinates', record, chunk_rows=16)
    """
    zarr = _provider()
    if (
        not isinstance(parent, zarr.Group)
        or not isinstance(record, QuantityRecord)
        or not isinstance(name, str)
        or not name
        or name in {".", ".."}
        or "/" in name
        or "\x00" in name
        or type(chunk_rows) is not int
        or chunk_rows <= 0
    ):
        raise RecordError(reason="Zarr write requires a group, record, direct child name and positive chunk_rows")
    if parent.metadata.zarr_format != 3:
        raise RecordError(reason="this snapshot binding requires Zarr format 3")
    if name in parent:
        raise RecordError(reason="Zarr write never overwrites an existing child", field=record.field)
    metadata = record.to_metadata()
    if metadata["manifest"]["format"] != "qrec/0.3":
        raise RecordError(reason="Zarr snapshots currently require homogeneous qrec/0.3")
    values = record.values
    chunks = () if values.ndim == 0 else (chunk_rows, *[max(1, n) for n in values.shape[1:]])
    headers = (
        [record.to_metadata()]
        if values.ndim == 0
        else [
            record.select(slice(start, start + chunk_rows)).to_metadata()
            for start in range(0, values.shape[0], chunk_rows)
        ]
    )
    node = {"format": FORMAT, "record": metadata, "physical_chunks": list(chunks), "chunks": headers}
    node["digest"] = metadata_digest(node)
    # No published group is readable before the final authoritative attribute.
    try:
        group = parent.create_group(name)
    except Exception as exc:
        raise RecordError(reason="cannot create the new Zarr child", field=record.field) from exc
    try:
        group.create_array("values", data=values, chunks=chunks, config={"write_empty_chunks": True})
        group.attrs.update({"units": record.unit, "pyunitwizard": json.dumps(node, allow_nan=False)})
    except Exception as exc:
        del parent[name]
        raise RecordError(reason="Zarr snapshot write failed; incomplete child removed", field=record.field) from exc
    return group


def read(
    group: Any,
    *,
    selection: Optional[slice] = None,
    field: Optional[str] = None,
    unit: Optional[str] = None,
    dimensionality: Optional[Dict[str, int]] = None,
    kind: Optional[str] = None,
) -> QuantityRecord:
    """Read a snapshot, verifying complete selected chunks before returning values.

    Parameters
    ----------
    group : zarr.Group
        Previously written binding; root/parent defaults are never consulted.
    selection : slice, optional
        Contiguous first-axis rows. Only intersecting chunks are read/verified;
        this does not certify unselected chunk contents.
    field, unit, dimensionality, kind : optional
        Reader expectations. At least ``unit`` or ``dimensionality`` is required.
        Units are validated here; conversion is explicit via ``to_quantity``.

    Returns
    -------
    QuantityRecord
        Original full snapshot or a newly sealed selected snapshot.

    Raises
    ------
    RecordError
        For integrity/expectation failures or unsupported selection.
    ModuleNotFoundError
        If Zarr is absent.

    Examples
    --------
    >>> subset = read(group, selection=slice(10, 20), field='coordinates', unit='nm')
    """
    zarr = _provider()
    if unit is None and dimensionality is None:
        raise RecordError(reason="a Zarr reader must declare unit or dimensionality")
    try:
        if not isinstance(group, zarr.Group) or set(group.keys()) != {"values"}:
            raise ValueError("snapshot children")
        node = json.loads(group.attrs["pyunitwizard"])
        digest = node.pop("digest")
        if node["format"] != FORMAT or metadata_digest(node) != digest:
            raise ValueError("binding seal")
        metadata = node["record"]
        manifest = metadata["manifest"]
        QuantityRecord.validate_metadata(metadata)
        array = group["values"]
        if (
            manifest["format"] != "qrec/0.3"
            or array.shards is not None
            or dict(array.attrs)
            or group.attrs["units"] != manifest["unit"]
            or list(array.shape) != manifest["shape"]
            or array.dtype.name != manifest["dtype"]
            or list(array.chunks) != node["physical_chunks"]
            or array.nchunks_initialized != array.nchunks
        ):
            raise ValueError("array or unit metadata")
        # Check reader expectations even for an empty selection, before I/O.
        probe = _record(np.empty(0, dtype=manifest["dtype"]), metadata)
        probe.to_quantity(field=field, unit=unit, dimensionality=dimensionality, kind=kind, form="pint")
        if not array.ndim:
            if selection is not None or len(node["chunks"]) != 1:
                raise ValueError("scalar selection")
            return QuantityRecord.from_array(np.asarray(array[()]), metadata=metadata)
        rows = array.shape[0]
        chunk_rows = array.chunks[0]
        if len(node["chunks"]) != (rows + chunk_rows - 1) // chunk_rows:
            raise ValueError("chunk inventory")
        if selection is not None and (not isinstance(selection, slice) or selection.step not in (None, 1)):
            raise ValueError("selection must have unit stride")
        start, stop, _ = (selection or slice(None)).indices(rows)
        stop = max(start, stop)
        parts = []
        for index in range(start // chunk_rows, (stop + chunk_rows - 1) // chunk_rows if stop > start else 0):
            lo, hi = index * chunk_rows, min((index + 1) * chunk_rows, rows)
            header = node["chunks"][index]
            cm = header["manifest"]
            if any(cm.get(k) != manifest.get(k) for k in ("format", "unit", "si", "dtype", "field", "kind")):
                raise ValueError("chunk unit/field association")
            if cm["shape"] != [hi - lo, *array.shape[1:]]:
                raise ValueError("chunk shape")
            chunk = QuantityRecord.from_array(np.asarray(array[slice(lo, hi)]), metadata=header)
            parts.append(chunk.values[max(start - lo, 0) : min(stop - lo, hi - lo)])
        values = np.concatenate(parts, axis=0) if parts else np.empty((0, *array.shape[1:]), dtype=array.dtype)
        return QuantityRecord.from_array(values, metadata=metadata) if selection is None else _record(values, metadata)
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason=f"invalid Zarr snapshot: {exc}", field=field) from exc
