"""Measure provisional record storage/layout operations on retained consumer data.

Run with the optional storage profile. Temporary stores are owned and removed by
each measurement. Tiled coordinates are synthetic stress data, not new MD frames.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import tempfile
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

import numpy as np

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord, QuantityRecordBundle
from pyunitwizard.storage import arrow
from pyunitwizard.storage import zarr as binding

ROOT = Path(__file__).resolve().parents[1]


def _measure(operation: Callable[[], Any], repeats: int = 3) -> list[float]:
    """Raw seconds per complete operation; no timing assertion or omitted first call."""
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        operation()
        samples.append(perf_counter() - start)
    return samples


def compare_storage(record: QuantityRecord, *, repeats: int = 3, chunk_rows: int = 32) -> dict[str, Any]:
    """Measure verified reads and immutable append versus full resealing.

    Parameters
    ----------
    record : QuantityRecord
        Homogeneous array with a first axis.
    repeats : int
        Raw samples per operation.
    chunk_rows : int
        Physical/verification chunk rows; partial selection reads one row.

    Returns
    -------
    dict
        Raw times, byte counts and scope. Parity is checked outside timing.

    Raises
    ------
    ValueError
        For scalar/empty data or an invalid repeat count.

    Examples
    --------
    >>> report = compare_storage(coordinate_record)
    """
    import zarr

    if repeats < 1 or record.values.ndim == 0 or record.values.shape[0] == 0:
        raise ValueError("nonempty array and positive repeats required")
    with tempfile.TemporaryDirectory(prefix="puw-storage-benchmark-") as directory:
        root = zarr.open_group(str(Path(directory) / "snapshot"), mode="w")
        start = perf_counter()
        group = binding.write(root, "values", record, chunk_rows=chunk_rows)
        write_zarr = perf_counter() - start
        path = Path(directory) / "values.parquet"
        start = perf_counter()
        arrow.write(path, record)
        write_parquet = perf_counter() - start
        table = arrow.to_table(record)
        selection = slice(0, 1)

        def full():
            return binding.read(group, field=record.field, unit=record.unit)

        def partial():
            return binding.read(group, selection=selection, field=record.field, unit=record.unit)

        assert full().digest == record.digest
        np.testing.assert_array_equal(partial().values, record.values[selection])
        assert arrow.from_table(table, unit=record.unit).digest == record.digest
        assert arrow.read(path, unit=record.unit).digest == record.digest
        incoming = puw.quantity(record.values[selection].copy(), record.unit, form="pint")

        def append():
            return record.append(incoming)

        def rebuild():
            return QuantityRecord.from_quantity(
                puw.quantity(np.concatenate((record.values, incoming.magnitude)), record.unit, form="pint"),
                field=record.field,
                kind=record.kind,
            )

        np.testing.assert_array_equal(append().values, rebuild().values)
        return {
            "shape": list(record.values.shape),
            "dtype": record.values.dtype.name,
            "unit": record.unit,
            "raw_bytes": record.values.nbytes,
            "zarr_bytes": sum(p.stat().st_size for p in (Path(directory) / "snapshot").rglob("*") if p.is_file()),
            "parquet_bytes": path.stat().st_size,
            "json_bytes": len(json.dumps(record.to_dict()).encode()),
            "chunk_rows": chunk_rows,
            "selected_rows": 1,
            "seconds": {
                "write_zarr_once": [write_zarr],
                "write_parquet_once": [write_parquet],
                "verified_zarr_full": _measure(full, repeats),
                "verified_zarr_partial": _measure(partial, repeats),
                "arrow_encode": _measure(lambda: arrow.to_table(record), repeats),
                "arrow_verify": _measure(lambda: arrow.from_table(table, unit=record.unit), repeats),
                "parquet_verify": _measure(lambda: arrow.read(path, unit=record.unit), repeats),
                "append": _measure(append, repeats),
                "concatenate_and_reseal": _measure(rebuild, repeats),
            },
        }


def main() -> None:
    """Emit provenance and observations; this is source qualification, not adoption."""
    coordinates_path = ROOT / "tests/data/h5msm_quantity_boundary.json"
    activity_path = ROOT / "tests/data/sabueso_activity_quantities.json"
    coordinates = json.loads(coordinates_path.read_text())
    activities = json.loads(activity_path.read_text())
    values = np.asarray(coordinates["values"], dtype=coordinates["dtype"])
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        cases = {}
        for tile in (1, 1024):
            q = puw.quantity(np.tile(values, (tile, 1, 1)), coordinates["unit"], form="pint")
            record = QuantityRecord.from_quantity(q, field="coordinates")
            cases[f"coordinates_tile_{tile}"] = compare_storage(record)
        rows = activities["observations"]
        quantities = [puw.quantity(r["value"], r["unit"], form="pint") for r in rows]
        kinds = [r["kind"] for r in rows]

        def build():
            return QuantityRecord.from_tagged(quantities, field="activities", kinds=kinds)

        tagged = build()

        def individuals():
            return [QuantityRecord.from_quantity(q, kind=k) for q, k in zip(quantities, kinds)]

        def bundles():
            return QuantityRecordBundle.from_quantities(
                {str(i): q for i, q in enumerate(quantities)}, kinds={str(i): k for i, k in enumerate(kinds)}
            )

        table = arrow.to_table(tagged)
        expected = {"units": ["nM", "nM", "percent", "nM", "nM"], "kinds": ["Ki", "IC50", "Inhibition", "Kd", "ED50"]}
        assert arrow.from_table(table, **expected).digest == tagged.digest
        tagged_report = {
            "observations": len(rows),
            "descriptors": len(tagged.descriptors),
            "json_bytes": {
                "tagged": len(json.dumps(tagged.to_dict()).encode()),
                "individual_records": len(json.dumps([r.to_dict() for r in individuals()]).encode()),
                "bundle": len(json.dumps(bundles().to_dict()).encode()),
            },
            "seconds": {
                "tagged_build": _measure(build),
                "individual_records": _measure(individuals),
                "bundle_build": _measure(bundles),
                "arrow_verify": _measure(lambda: arrow.from_table(table, **expected)),
            },
        }
        with tempfile.TemporaryDirectory(prefix="puw-tagged-parquet-") as directory:
            path = Path(directory) / "activities.parquet"
            start = perf_counter()
            arrow.write(path, tagged)
            tagged_report["seconds"]["parquet_write_once"] = [perf_counter() - start]
            assert arrow.read(path, **expected).digest == tagged.digest
            tagged_report["parquet_bytes"] = path.stat().st_size
            tagged_report["seconds"]["parquet_verify"] = _measure(lambda: arrow.read(path, **expected))
    sources = [
        "pyunitwizard/record.py",
        "pyunitwizard/_tagged_record.py",
        "pyunitwizard/storage/zarr.py",
        "pyunitwizard/storage/arrow.py",
        "devtools/benchmark_record_extensions.py",
    ]
    report = {
        "schema": "pyunitwizard.record-extensions-benchmark@1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "git_describe": subprocess.check_output(
            ["git", "describe", "--always", "--dirty"], cwd=ROOT, text=True
        ).strip(),
        "versions": {name: version(name) for name in ["numpy", "pint", "zarr", "pyarrow"]},
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources},
        "inputs": {
            "coordinates": coordinates,
            "activities_provenance": activities["source"],
            "activities_sha256": hashlib.sha256(activity_path.read_bytes()).hexdigest(),
        },
        "scope": "Source checkout; consumer-derived fixtures, no consumer code migration. Coordinate tile 1024 is synthetic repeated data; local serial operations, first calls retained, reads warmed after parity checks. No universal speedup or published-artifact qualification.",
        "coordinates": cases,
        "activities": tagged_report,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
