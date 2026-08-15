from __future__ import annotations

import json
from contextlib import contextmanager
from datetime import datetime, timezone
from statistics import median
from time import perf_counter
from typing import Callable, Dict, Iterator, List

import smonitor

import pyunitwizard as puw
from pyunitwizard.parse import parse as parse_quantity


def _time_block(func: Callable[[], None], iterations: int) -> float:
    t0 = perf_counter()
    for _ in range(iterations):
        func()
    t1 = perf_counter()
    return (t1 - t0) / iterations


@contextmanager
def _telemetry(enabled: bool) -> Iterator[None]:
    """Pin SMonitor to a known state for the duration of a measurement block.

    Telemetry is enabled by default on import, so an unpinned benchmark
    measures whatever ambient configuration it inherits. Both modes are timed
    separately because their difference is the quantity worth watching: the
    instrumentation cost carried by the path users actually run.
    """

    manager = smonitor.get_manager()
    previous = getattr(manager, "enabled", True)
    smonitor.configure(enabled=enabled, handlers=[])
    try:
        yield
    finally:
        smonitor.configure(enabled=previous, handlers=[])


def _measure(
    benchmarks: Dict[str, Callable[[], None]],
    iterations: int,
    repeats: int,
) -> Dict[str, Dict[str, float]]:
    results: Dict[str, Dict[str, float]] = {}

    for name, func in benchmarks.items():
        samples: List[float] = [_time_block(func, iterations) for _ in range(repeats)]
        results[name] = {
            "median_seconds": median(samples),
            "min_seconds": min(samples),
            "max_seconds": max(samples),
        }

    return results


def run_baseline(iterations: int = 5000, repeats: int = 5) -> Dict[str, object]:
    """Run a small deterministic performance baseline for hot API paths.

    Every case is timed twice: once with telemetry enabled, which is the mode a
    real user runs in, and once with it disabled. Subtracting the two gives the
    instrumentation cost per case, which is otherwise invisible.
    """

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nanometer", "picosecond", "kilocalorie", "mole"])

    quantity = puw.quantity(1.0, "nanometer")
    quantity_si = puw.quantity(1.0, "meter")
    unit = puw.unit("nanometer", form="pint")

    benchmarks: Dict[str, Callable[[], None]] = {
        "convert_nm_to_angstrom": lambda: puw.convert(quantity, to_unit="angstrom"),
        "get_value_nm_to_angstrom": lambda: puw.get_value(
            quantity, to_unit="angstrom"
        ),
        "get_form_quantity": lambda: puw.get_form(quantity),
        "is_quantity_quantity": lambda: puw.is_quantity(quantity),
        "parse_string_quantity": lambda: puw.quantity("10 angstrom"),
        "parse_array_string_quantity": lambda: parse_quantity("[1, 2, 3] angstrom", to_form="pint"),
        "get_dimensionality_quantity": lambda: puw.get_dimensionality(quantity),
        "get_dimensionality_unit": lambda: puw.get_dimensionality(unit),
        "standardize_meter_quantity": lambda: puw.standardize(quantity_si),
    }

    with _telemetry(enabled=True):
        results = _measure(benchmarks, iterations, repeats)

    with _telemetry(enabled=False):
        results_telemetry_disabled = _measure(benchmarks, iterations, repeats)

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": "3.13",
        "iterations": iterations,
        "repeats": repeats,
        # Read from installed distribution metadata. For a development
        # checkout this reports the last install, not the working tree, so
        # pair it with `git describe --tags --always` when recording these
        # numbers as provenance in devguide documents.
        "versions": _installed_versions(),
        "results": results,
        "results_telemetry_disabled": results_telemetry_disabled,
    }


def _installed_versions() -> Dict[str, str]:
    """Return installed versions of the packages whose cost these numbers mix."""

    from importlib.metadata import PackageNotFoundError, version

    versions = {}
    for package in ("pyunitwizard", "pint", "smonitor", "depdigest"):
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "not installed"

    return versions


if __name__ == "__main__":
    output = run_baseline()
    print(json.dumps(output, indent=2, sort_keys=True))
