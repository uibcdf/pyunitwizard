# Pandas Interoperability

## Motivation

Many scientific workflows rely on pandas DataFrames for data analysis.

However, pandas does not natively support quantities with units.
This often leads to:

- units being dropped
- quantities converted to object dtype
- inconsistent handling across workflows

## Design Goal

PyUnitWizard should provide utilities to safely integrate quantities
with pandas structures.

## Possible Interfaces

- `pyunitwizard.utils.pandas.dataframe_from_quantities(...)`
- `pyunitwizard.utils.pandas.add_quantity_column(...)`
- `pyunitwizard.utils.pandas.get_quantity_column(...)`
- `pyunitwizard.utils.pandas.get_units_map(...)`
- `pyunitwizard.utils.pandas.set_units_map(...)`
- `pyunitwizard.utils.pandas.sync_units_map(...)`
- `pyunitwizard.utils.pandas.concat(...)`
- `pyunitwizard.utils.pandas.merge(...)`

## Current Status

Initial implementation is available in `pyunitwizard.utils.pandas` and covered
by tests in:
- `tests/utils/pandas/test_frame_contract.py`
- `tests/utils/pandas/test_workflows.py`

The current contract is intentionally explicit: standard pandas workflows are
preserved, and users call PyUnitWizard only at the conversion boundaries.

Transparent mode is also available:
- `pyunitwizard.utils.pandas.setup_pandas(enable=True)` injects `DataFrame.puw`.
- `df.puw.get_quantity(...)` and `df.puw.set_quantity(...)` provide explicit
  quantity round-trip at table boundaries while keeping normal pandas usage.
- `df.puw.get_units_map()`, `df.puw.set_units_map(...)`,
  `df.puw.sync_units_map(...)` manage metadata as dataframe operations evolve.

## Benefits

- safer data science workflows
- explicit unit handling in tabular data
- improved integration with analytics pipelines
