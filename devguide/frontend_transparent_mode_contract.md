# Frontend Transparent Mode Contract (Pre-1.0)

This document defines the contract for transparent frontend integrations:
- `pyunitwizard.utils.numpy.setup_numpy` / `numpy_context`
- `pyunitwizard.utils.pandas.setup_pandas` / `pandas_context`
- `pyunitwizard.utils.matplotlib.setup_matplotlib` / `plotting_context`

## Purpose

Allow users to keep standard frontend imports (`numpy`, `pandas`,
`matplotlib`) while enabling quantity-aware behavior in controlled workflows.

## Contract

1. Opt-in only
- Transparent behavior is enabled only after explicit setup/context calls.

2. Reversible
- `setup_*(enable=False)` restores previous behavior.
- Context managers restore previous state on exit, including exception paths.

3. Idempotent setup
- Repeated `setup_*(enable=True)` calls are safe.
- Repeated `setup_*(enable=False)` calls are safe.

4. Quantity-dispatch only
- Quantity inputs dispatch to PyUnitWizard-aware routes.
- Plain numeric inputs keep native frontend behavior.

5. No hidden global configuration mutation
- Transparent mode must not mutate PyUnitWizard runtime configuration
  (default parser/form/units) as side effect.

## Known risk surface

1. Global patching scope
- Transparent mode for `numpy`/`pandas` relies on runtime patching and is
  process-global for the patched symbols.

2. Third-party interaction
- Other libraries patching the same symbols may conflict.
- Integrators should scope usage with context managers when possible.

## Pre-1.0 evidence requirement

- Test evidence for:
  - enable/disable lifecycle,
  - context restoration,
  - mixed backend quantity paths,
  - no-regression path for plain numeric inputs.
