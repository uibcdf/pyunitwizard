# PyUnitWizard package guidelines

This file covers the public package that ships to users. Follow these notes whenever you edit files in this directory tree.

## Import side effects and kernel lifecycle
- Importing `pyunitwizard` runs `pyunitwizard.__init__`, which calls `kernel.initialize()` and immediately attempts to load every supported library (`pint`, `openmm.unit`, `unyt`, `astropy.units`) if the corresponding Python packages can be imported.
- Any module-level import of `pyunitwizard.main` or symbols re-exported in `__init__` therefore assumes the kernel has been initialized and the default form/parser have been set.
- Keep the initialization idempotent. Re-importing the package must not mutate global state unexpectedly or require additional configuration from users.

## Default library loading expectations
- Default library probing is part of the user experience. Only adjust the eager import-and-load logic when the change has been reviewed for backward compatibility and documented for users.
- When adding, removing, or reordering default libraries make sure tests cover the new behavior and the README in this directory is updated.
- Avoid importing optional heavy dependencies at module import time. All new optional integrations should use the same `configure.load_library` path.

## Top-level API stability
- Files `main.py`, `parse.py`, `kernel.py`, and the `configure` package form the primary public API that is re-exported from `pyunitwizard.__init__`.
- Do not rename or remove existing functions without deprecation shims.
- Keep function signatures backward compatible. Add new parameters as keyword-only when possible.
- Document any user-facing change in `pyunitwizard/pyunitwizard/README.md` and update tests to reflect the new behavior.

## Testing expectations
- Run the relevant pytest targets (at minimum `pytest tests`) after editing these modules.
- Add regression tests whenever you fix a bug or change default initialization.
