"""Provisional qrec-arrow/0.1 binding for typed Arrow tables and local Parquet.

One table owns its values, optional descriptor codes and authoritative sealed
schema metadata. Nulls are refused: qrec has no missing-value bitmap; NaN/Inf
remain numeric values. This binding does not infer pandas or domain schemas.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np

from pyunitwizard.record import QuantityRecord, RecordError, metadata_digest

FORMAT = "qrec-arrow/0.1"
_KEY = b"pyunitwizard"


def _provider():
    from depdigest import is_installed

    if not is_installed("pyarrow"):
        raise ModuleNotFoundError("Install optional Arrow tools with conda install -c conda-forge pyarrow=25.0.0")
    import pyarrow

    return pyarrow


def to_table(record: QuantityRecord) -> Any:
    """Encode one homogeneous or tagged record in one Arrow table.

    Parameters
    ----------
    record : QuantityRecord
        Sealed scalar or array; original shape is retained in schema metadata.

    Returns
    -------
    pyarrow.Table
        Flattened typed values, optional uint16 codes, and a verified manifest.

    Raises
    ------
    RecordError
        For a non-record source.
    ModuleNotFoundError
        If PyArrow is absent.

    Examples
    --------
    >>> table = to_table(record)
    """
    pa = _provider()
    if not isinstance(record, QuantityRecord):
        raise RecordError(reason="Arrow encoding requires a sealed QuantityRecord")
    metadata = record.to_metadata()
    metadata.pop("codes", None)
    node = {"format": FORMAT, "record": metadata}
    node["digest"] = metadata_digest(node)
    arrays = [pa.array(record.values.reshape(-1), type=pa.from_numpy_dtype(record.values.dtype), from_pandas=False)]
    fields = [pa.field("values", arrays[0].type, nullable=False)]
    if record.layout == "tagged":
        arrays.append(pa.array(record.codes.reshape(-1), type=pa.uint16()))
        fields.append(pa.field("codes", pa.uint16(), nullable=False))
    schema = pa.schema(fields, metadata={_KEY: json.dumps(node, allow_nan=False).encode("utf-8")})
    return pa.Table.from_arrays(arrays, schema=schema)


def from_table(
    table: Any,
    *,
    field: Optional[str] = None,
    unit: Optional[str] = None,
    dimensionality: Optional[Dict[str, int]] = None,
    kind: Optional[str] = None,
    units: Optional[Sequence[str]] = None,
    kinds: Optional[Sequence[Optional[str]]] = None,
) -> QuantityRecord:
    """Verify a complete table and the reader's explicit unit expectations.

    Parameters
    ----------
    table : pyarrow.Table
        Complete binding table; column projection alone is not a verified record.
    field, unit, dimensionality, kind : optional
        Homogeneous reader handshake; unit or dimensionality is required.
    units : sequence of str, optional
        Tagged-only expected unit per local descriptor code, in table order.
    kinds : sequence of str or None, optional
        Tagged-only expected kind per descriptor. No kinds are inferred.

    Returns
    -------
    QuantityRecord
        Original inert record with unchanged values, units and seal. Convert
        explicitly through ``to_quantity`` or ``split`` after reading.

    Raises
    ------
    RecordError
        For missing/conflicting metadata, nulls, altered values/codes or expectations.
    ModuleNotFoundError
        If PyArrow is absent.

    Examples
    --------
    >>> restored = from_table(table, field='coordinates', unit='nm')
    """
    pa = _provider()
    try:
        if not isinstance(table, pa.Table):
            raise ValueError("not an Arrow table")
        node = json.loads(table.schema.metadata[_KEY])
        digest = node.pop("digest")
        if node["format"] != FORMAT or metadata_digest(node) != digest:
            raise ValueError("binding seal")
        metadata = node["record"]
        manifest = metadata["manifest"]
        tagged = manifest.get("layout") == "tagged"
        expected = ["values", "codes"] if tagged else ["values"]
        if table.column_names != expected or any(f.metadata for f in table.schema):
            raise ValueError("columns or secondary metadata")
        if any(c.null_count for c in table.columns):
            raise ValueError("nulls are not NaN and cannot be represented by qrec")
        values = table["values"].combine_chunks().to_numpy(zero_copy_only=False).reshape(manifest["shape"])
        if tagged:
            codes = table["codes"].combine_chunks().to_numpy(zero_copy_only=False)
            if codes.dtype != np.dtype("uint16"):
                raise ValueError("descriptor-code dtype")
            metadata["codes"] = codes.reshape(manifest["shape"]).tolist()
        record = QuantityRecord.from_array(values, metadata=metadata)
        if tagged:
            if unit is not None or dimensionality is not None or kind is not None:
                raise ValueError("tagged readers require per-descriptor units/kinds")
            if units is None or len(units) != len(record.descriptors):
                raise ValueError("expected unit per descriptor is required")
            if kinds is not None and len(kinds) != len(record.descriptors):
                raise ValueError("expected kind per descriptor")
            for index, group in record.split().items():
                if kinds is not None and group.kind != kinds[index]:
                    raise ValueError("descriptor kind")
                group.to_quantity(field=field, unit=units[index], form="pint")
        else:
            if units is not None or kinds is not None or (unit is None and dimensionality is None):
                raise ValueError("homogeneous reader requires unit or dimensionality")
            record.to_quantity(field=field, unit=unit, dimensionality=dimensionality, kind=kind, form="pint")
        return record
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason=f"invalid Arrow record: {exc}", field=field) from exc


def write(path: Any, record: QuantityRecord) -> None:
    """Publish a new local Parquet file without overwriting an existing path.

    Parameters
    ----------
    path : path-like
        New local filesystem path. Parent directory must already exist.
    record : QuantityRecord
        Homogeneous or tagged source, encoded with ``to_table``.

    Returns
    -------
    None

    Raises
    ------
    RecordError
        For an existing path or a failed write. Owned staging files are removed.
    ModuleNotFoundError
        If PyArrow is absent.

    Examples
    --------
    >>> write('coordinates.parquet', record)
    """
    table = to_table(record)
    import pyarrow.parquet as pq

    target = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=target.parent, prefix=".qrec-", suffix=".parquet", delete=False
        ) as handle:
            temporary = Path(handle.name)
        pq.write_table(table, temporary, store_schema=True)
        # Same-directory hard link is an atomic exclusive publication on local filesystems.
        os.link(temporary, target)
    except Exception as exc:
        raise RecordError(reason=f"Parquet publication failed: {exc}") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def read(path: Any, **expectations: Any) -> QuantityRecord:
    """Read one complete local Parquet binding through ``from_table``.

    Parameters
    ----------
    path : path-like
        Complete local Parquet file, not a partitioned dataset.
    **expectations
        Explicit reader handshake accepted by ``from_table``.

    Returns
    -------
    QuantityRecord
        Verified inert snapshot.

    Raises
    ------
    RecordError
        For a corrupt/unsupported file or failed reader expectations.
    ModuleNotFoundError
        If PyArrow is absent.

    Examples
    --------
    >>> restored = read('coordinates.parquet', unit='nm')
    """
    _provider()
    import pyarrow.parquet as pq

    try:
        table = pq.ParquetFile(path).read()
    except Exception as exc:
        raise RecordError(reason=f"Parquet read failed: {exc}") from exc
    return from_table(table, **expectations)
