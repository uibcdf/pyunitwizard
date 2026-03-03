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
- `string` form

Runtime loading of available backends/parsers is handled via configuration.

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

PyUnitWizard is in pre-1.0 stabilization. The `0.19.x` line is treated as the
release-candidate (RC) window before the stable `1.0.0` tag.
Current release planning and milestones are tracked in `devguide/`.

PyUnitWizard aims to become a units interoperability layer for Scientific Python.

## Ecosystem

PyUnitWizard is part of the current UIBCDF interoperability stack:
- [ArgDigest](https://github.com/uibcdf/argdigest)
- [DepDigest](https://github.com/uibcdf/depdigest)
- [SMonitor](https://github.com/uibcdf/smonitor)

## License

MIT. See [LICENSE](LICENSE).
