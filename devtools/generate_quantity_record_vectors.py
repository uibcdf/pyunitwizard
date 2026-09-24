"""Regenerate the published QuantityRecord test vectors (tests/quantity_record_vectors/).

The vectors freeze the format: tests assert that the library reproduces them byte for
byte, and third parties use them to check their own readers. The expected SI values are
written by hand here, independently of the implementation. Regenerate only with a format
version change, and say so in the changelog.
"""

import json
from pathlib import Path

import numpy as np

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

FOLDER = Path(__file__).resolve().parents[1] / "tests" / "quantity_record_vectors"

CASES = {
    "scalar_concentration_with_kind": (
        puw.quantity(3.0, "nM", form="pint"),
        "bioactivity.ic50",
        "http://qudt.org/vocab/quantitykind/AmountOfSubstanceConcentration",
        [3.0e-6],  # 3 nmol/L = 3e-9 mol / 1e-3 m^3
    ),
    "coordinates_float32_2d": (
        puw.quantity(np.array([[0.5, 1.0, 1.5], [2.0, 2.5, 3.0]], dtype=np.float32), "nm", form="pint"),
        "structures.coordinates",
        None,
        [0.5e-9, 1.0e-9, 1.5e-9, 2.0e-9, 2.5e-9, 3.0e-9],
    ),
    "counts_int32_dalton": (
        puw.quantity(np.array([180, 18], dtype=np.int32), "dalton", form="pint"),
        "properties.molecular_weight",
        None,
        [180 * 1.66053906892e-27, 18 * 1.66053906892e-27],
    ),
    "affine_celsius": (
        puw.quantity(np.array([20.0, 37.0]), "degC", form="pint"),
        "assay.temperature",
        None,
        [293.15, 310.15],
    ),
    "compound_unit": (
        puw.quantity(np.array([1.0e-3]), "N*s/m**2", form="pint"),
        "fluid.viscosity",
        None,
        [1.0e-3],
    ),
}


def main() -> None:
    FOLDER.mkdir(parents=True, exist_ok=True)
    for name, (quantity, field, kind, si_values) in CASES.items():
        record = QuantityRecord.from_quantity(quantity, field=field, kind=kind)
        case = {"record": record.to_dict(), "si_values": si_values}
        (FOLDER / f"{name}.json").write_text(json.dumps(case, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
