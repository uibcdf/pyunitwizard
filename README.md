# PyUnitWizard

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/uibcdf/pyunitwizard/actions/workflows/CI.yaml/badge.svg)](https://github.com/uibcdf/pyunitwizard/actions/workflows/CI.yaml)
[![Documentation](https://github.com/uibcdf/pyunitwizard/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://github.com/uibcdf/pyunitwizard/actions/workflows/sphinx_docs_to_gh_pages.yaml)
[![codecov](https://codecov.io/github/uibcdf/pyunitwizard/graph/badge.svg?token=9ZMA4YZLOR)](https://codecov.io/github/uibcdf/pyunitwizard)
[![Install with conda](https://img.shields.io/badge/Install%20with-conda-brightgreen.svg)](https://conda.anaconda.org/uibcdf/pyunitwizard)

*A Python Units Wizard that streamlines work with physical quantities.*

## Overview

**PyUnitWizard** is a compatibility layer for working with physical quantities
across multiple unit libraries through one consistent API.

It is designed for scientific Python projects that need to:
- accept heterogeneous quantity inputs,
- convert and compare quantities deterministically,
- keep stable unit contracts at API boundaries.

## Why adopt PyUnitWizard

- One public API for quantity construction, conversion, validation, and normalization.
- Easier interoperability between libraries that use different unit backends.
- Explicit dimensional checks and compatibility checks in integration code.
- Stable unit behavior that is easier to test and document.

## Installation

Recommended:

```bash
conda install -c uibcdf pyunitwizard
```

Alternative:

```bash
pip install pyunitwizard
```

## Quick start

```python
import pyunitwizard as puw

puw.configure.reset()
puw.configure.load_library(["pint"])
puw.configure.set_default_form("pint")
puw.configure.set_default_parser("pint")
puw.configure.set_standard_units(["nm", "ps", "kcal", "mole"])

distance = puw.quantity(1.0, "nanometer")
distance_angstrom = puw.convert(distance, to_unit="angstrom")

print(puw.to_string(distance_angstrom))
print(puw.are_compatible(distance, distance_angstrom))
```

## Core capabilities

- Quantity and unit construction: `quantity`, `unit`
- Conversion and formatting: `convert`, `to_string`
- Validation and comparison: `check`, `are_compatible`, `are_close`, `are_equal`
- Introspection and extraction: `get_form`, `get_dimensionality`, `get_value`, `get_unit`
- Standardization: `standardize`, `get_standard_units`
- Runtime configuration: `pyunitwizard.configure.*`

## Backend support

PyUnitWizard supports interoperation with:
- `pint`
- `openmm.unit`
- `unyt`
- `astropy.units`
- `physipy`
- `quantities`
- `string` form

Runtime loading of available backends/parsers is handled via configuration.
Dependency policy:
- hard runtime dependency: `pint`;
- optional runtime dependencies: `openmm.unit`, `unyt`, `astropy.units`,
  `physipy`, `quantities`.

Objects supported in practice:
- quantities from all listed backends;
- unit objects from backends that expose distinct unit types (`pint`,
  `openmm.unit`, `unyt`, `astropy.units`);
- unit-like scalar objects for backends where unit/quantity share the same type
  (`physipy`, `quantities`).

String parser support:
- parser-capable: `pint`, `astropy.units`;
- explicit parser-not-supported errors: `openmm.unit`, `unyt`, `physipy`,
  `quantities`.

Matplotlib transparent integration:
- Keep using standard `matplotlib` imports.
- Enable unit-aware plotting for mixed backend quantities with:

```python
import pyunitwizard as puw
puw.utils.matplotlib.setup_matplotlib()
```

NumPy transparent integration:
- Keep using standard `numpy` imports.
- Enable quantity-aware dispatch for common operations (`mean`, `sum`, `std`,
  `var`, `dot`, `linalg.norm`, `trapezoid`) with:

```python
import numpy as np
import pyunitwizard as puw

puw.utils.numpy.setup_numpy(enable=True)
result = np.mean(puw.quantity([1.0, 2.0, 3.0], "meter"))
```

Explicit NumPy wrappers are also available in `puw.utils.numpy`
(`mean`, `sum`, `std`, `var`, `dot`, `linalg_norm`, `trapz`).

Pandas interoperability helpers:
- Keep using standard `pandas` imports.
- Optional transparent accessor for DataFrames: `df.puw.*`.
- Metadata-preserving table helpers are available: `concat`, `merge`,
  `set_units_map`, `sync_units_map`.

```python
import pyunitwizard as puw

puw.utils.pandas.setup_pandas(enable=True)
df = puw.utils.pandas.dataframe_from_quantities(
    {"length": puw.quantity([1.0, 2.0], "nanometer")}
)
q = df.puw.get_quantity("length")
```

Matplotlib coverage highlights:
- transparent bridge for supported quantity backends;
- mixed-backend plotting on compatible axes;
- advanced layout scenarios (shared axes, twin axes, multi-series overlays)
  covered by tests.

## Diagnostics (SMonitor)

PyUnitWizard integrates with **SMonitor** for structured diagnostics.
Runtime SMonitor configuration is loaded from:
- `pyunitwizard/_smonitor.py`
- `pyunitwizard/_private/smonitor/catalog.py`
- `pyunitwizard/_private/smonitor/meta.py`

## Documentation

- Website: https://www.uibcdf.org/pyunitwizard
- User guide: `docs/content/user/`
- Developer guide: `docs/content/developer/`
- API reference: `docs/api/`
- Consolidation roadmap: `devguide/roadmap.md`

## Development

Run tests:

```bash
pytest -q
```

Build docs:

```bash
make -C docs html
```

## Status

PyUnitWizard is in pre-1.0 stabilization. The `0.19.x` line is treated as a
historical checkpoint, `0.20.x` as interoperability expansion, and `0.21.x` as
the RC consolidation window before the stable `1.0.0` tag.
Current release planning and milestones are tracked in `devguide/`.

PyUnitWizard aims to become a units interoperability layer for Scientific Python.

## Ecosystem

PyUnitWizard is part of the current UIBCDF interoperability stack:
- [ArgDigest](https://github.com/uibcdf/argdigest)
- [DepDigest](https://github.com/uibcdf/depdigest)
- [SMonitor](https://github.com/uibcdf/smonitor)

## License

MIT. See [LICENSE](LICENSE).
