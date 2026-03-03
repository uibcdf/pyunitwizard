from __future__ import annotations

import json
from datetime import datetime, timezone
from statistics import median
from time import perf_counter
from typing import Callable, Dict, List

import pyunitwizard as puw


def _time_block(func: Callable[[], None], iterations: int) -> float:
    t0 = perf_counter()
    for _ in range(iterations):
        func()
    t1 = perf_counter()
    return (t1 - t0) / iterations


def run_baseline(iterations: int = 5000, repeats: int = 5) -> Dict[str, object]:
    """Run a small deterministic performance baseline for hot API paths."""

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")

    quantity = puw.quantity(1.0, "nanometer")

    benchmarks: Dict[str, Callable[[], None]] = {
        "convert_nm_to_angstrom": lambda: puw.convert(quantity, to_unit="angstrom"),
        "get_form_quantity": lambda: puw.get_form(quantity),
        "is_quantity_quantity": lambda: puw.is_quantity(quantity),
        "parse_string_quantity": lambda: puw.quantity("10 angstrom"),
    }

    results: Dict[str, Dict[str, float]] = {}

    for name, func in benchmarks.items():
        samples: List[float] = [_time_block(func, iterations) for _ in range(repeats)]
        results[name] = {
            "median_seconds": median(samples),
            "min_seconds": min(samples),
            "max_seconds": max(samples),
        }

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": "3.13",
        "iterations": iterations,
        "repeats": repeats,
        "results": results,
    }


if __name__ == "__main__":
    output = run_baseline()
    print(json.dumps(output, indent=2, sort_keys=True))
