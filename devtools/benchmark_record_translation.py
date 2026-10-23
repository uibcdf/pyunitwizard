"""Compare live conversion, record construction and stored-record reading (#106).

Run from an environment containing PyUnitWizard and the selected optional backends.
Timing is warmed, local evidence; it does not qualify an installed public artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import subprocess
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Dict, Optional

import numpy as np
import smonitor

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

ROOT = Path(__file__).resolve().parents[1]


def _parity(output: Any, expected: np.ndarray, unit: str) -> Dict[str, Any]:
    if puw.has_unit(output, unit) is not True:
        raise AssertionError("translation did not produce the negotiated unit")
    values = np.asarray(puw.get_value(output))
    if values.shape != expected.shape:
        raise AssertionError("translation changed shape")
    if values.dtype != expected.dtype:
        raise AssertionError("translation changed dtype")
    np.testing.assert_allclose(values, expected, rtol=1e-6, atol=1e-12)
    difference = np.abs(values.astype(float) - expected.astype(float))
    return {
        "shape": list(values.shape),
        "dtype": values.dtype.name,
        "max_abs_error": float(difference.max()) if difference.size else 0.0,
        "preview": values.reshape(-1)[:3].tolist(),
    }


def _measure(paths: Dict[str, Callable[[], Any]], iterations: int, repeats: int) -> Dict[str, Any]:
    samples = {name: [] for name in paths}
    names = list(paths)
    for repeat in range(repeats):
        # Rotate order to avoid always assigning one route the first time slot.
        for name in names[repeat % len(names) :] + names[: repeat % len(names)]:
            operation = paths[name]
            start = perf_counter()
            for _ in range(iterations):
                operation()
            samples[name].append((perf_counter() - start) / iterations)
    return {
        name: {"samples_seconds": measured, "median_seconds": statistics.median(measured)}
        for name, measured in samples.items()
    }


def compare_translation(
    quantity: Any,
    target_form: str,
    target_unit: str,
    *,
    field: Optional[str] = None,
    kind: Optional[str] = None,
    iterations: int = 100,
    repeats: int = 7,
) -> Dict[str, Any]:
    """Measure four conversion cost scopes after checking their numerical parity.

    Parameters
    ----------
    quantity : quantity
        Finite scalar or array quantity in a supported live backend.
    target_form, target_unit : str
        Explicit computing backend and negotiated target unit.
    field, kind : str, optional
        Record binding and reader expectations, retained on all record routes.
    iterations, repeats : int
        Positive calls per sample and number of raw timing samples.

    Returns
    -------
    dict
        Input description, parity and raw seconds per operation in both telemetry
        modes. ``via_record`` pays construction; ``read_existing`` starts after
        verification; ``read_wire`` includes base64 decoding and seal checks.

    Raises
    ------
    ValueError
        For invalid counts, nonfinite inputs or conflicting registry definitions.
    AssertionError
        If a route changes negotiated unit, shape, dtype or numerical meaning.
    Exception
        Backend/conversion and measurement errors propagate; policy and telemetry
        enabled state are restored, including on failure.

    Examples
    --------
    >>> q = puw.quantity([1.0, 2.0], "angstrom", form="pint")
    >>> report = compare_translation(q, "pint", "nanometer", iterations=1, repeats=1)
    """
    if any(not isinstance(value, int) or value <= 0 for value in (iterations, repeats)):
        raise ValueError("iterations and repeats must be positive integers")
    manager = smonitor.get_manager()
    previous_enabled = manager.enabled
    with puw.context(default_form="pint", default_parser="pint"):
        try:
            # An explicit Pint reference precedes all timed routes.
            reference = puw.convert(quantity, to_form="pint", to_unit=target_unit)
            expected = np.asarray(puw.get_value(reference))
            if not np.isfinite(expected).all():
                raise ValueError("the benchmark accepts finite quantities only")
            stored = QuantityRecord.from_quantity(quantity, field=field, kind=kind)
            wire = stored.to_dict(encoding="base64")
            expectations = {"field": field, "kind": kind, "form": target_form, "unit": target_unit}
            paths = {
                "direct": lambda: puw.convert(quantity, to_form=target_form, to_unit=target_unit),
                "via_record": lambda: QuantityRecord.from_quantity(quantity, field=field, kind=kind).to_quantity(
                    **expectations
                ),
                "read_existing": lambda: stored.to_quantity(**expectations),
                "read_wire": lambda: QuantityRecord.from_dict(wire).to_quantity(**expectations),
            }
            results = {}
            for enabled in (True, False):
                smonitor.configure(enabled=enabled)
                parity = {name: _parity(operation(), expected, target_unit) for name, operation in paths.items()}
                measured = _measure(paths, iterations, repeats)
                for name in paths:
                    _parity(paths[name](), expected, target_unit)
                    measured[name]["parity"] = parity[name]
                results["telemetry_enabled" if enabled else "telemetry_disabled"] = measured
            return {
                "input": {
                    "form": puw.get_form(quantity),
                    "unit": stored.unit,
                    "shape": list(stored.values.shape),
                    "dtype": stored.values.dtype.name,
                    "field": field,
                    "kind": kind,
                },
                "target": {"form": target_form, "unit": target_unit},
                "iterations": iterations,
                "repeats": repeats,
                "results": results,
            }
        finally:
            smonitor.configure(enabled=previous_enabled)


def main() -> None:
    """Emit JSON evidence for the published TopoMT coordinate fixture and an affine control."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=ROOT / "tests/data/topomt_quantity_records.json")
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument(
        "--tile", type=int, default=1, help="repeat the coordinate array; >1 is a synthetic scaling control"
    )
    args = parser.parse_args()
    if args.tile < 1:
        parser.error("--tile must be positive")
    fixture_bytes = args.fixture.read_bytes()
    fixture = json.loads(fixture_bytes)
    record = QuantityRecord.from_dict(fixture["records"]["coordinates"])
    with puw.context(default_form="pint", default_parser="pint"):
        coordinates = puw.quantity(np.tile(record.values, (args.tile, 1)), record.unit, form="pint")
        cases = {}
        for source, target in (("pint", "openmm.unit"), ("openmm.unit", "unyt"), ("unyt", "astropy.units")):
            quantity = puw.convert(coordinates, to_form=source)
            cases[f"coordinates_{source}_to_{target}"] = compare_translation(
                quantity, target, "nanometer", field="coordinates", iterations=args.iterations, repeats=args.repeats
            )
        temperature = puw.quantity(np.array([-10.0, 0.0, 25.0], dtype=np.float32), "degree_Celsius", form="pint")
        cases["affine_control_pint_to_unyt"] = compare_translation(
            temperature, "unyt", "kelvin", field="temperature", iterations=args.iterations, repeats=args.repeats
        )
    versions = {}
    for package in (
        "pyunitwizard",
        "numpy",
        "pint",
        "openmm",
        "unyt",
        "astropy",
        "smonitor",
        "depdigest",
        "argdigest",
    ):
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "not installed"
    sources = [
        "devtools/benchmark_record_translation.py",
        "pyunitwizard/record.py",
        "pyunitwizard/api/conversion.py",
        *[f"pyunitwizard/forms/api_{name}.py" for name in ("pint", "openmm_unit", "unyt", "astropy_unit")],
    ]
    output = {
        "schema": "pyunitwizard.record-translation-benchmark@1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "versions": versions,
        "git_describe": subprocess.check_output(
            ["git", "describe", "--tags", "--always", "--dirty"], cwd=ROOT, text=True
        ).strip(),
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources},
        "input_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "input_provenance": fixture["source"],
        "coordinate_tile": args.tile,
        "scope": "warmed source-checkout evaluation; not cold-import, client adoption or installed-artifact qualification",
        "method": "rotating route order; raw seconds per operation; setup, reference and parity outside timing; both telemetry modes",
        "cases": cases,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
