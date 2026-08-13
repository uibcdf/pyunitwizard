# PyUnitWizard package guidelines

This file covers the public package that ships to users. Follow these notes whenever you edit files in this directory tree.

## Import side effects and kernel lifecycle
- Importing `pyunitwizard` runs `pyunitwizard.__init__`, which calls `kernel.initialize()` but does not import optional unit backends.
- Backends are discovered and loaded on first demand through `digest_form` and `configure.load_library`; importing an external quantity should load only its matching adapter.
- Any module-level import of `pyunitwizard.main` or symbols re-exported in `__init__` assumes the kernel has been initialized, but the default form/parser may remain unset until the first backend is requested.
- Keep the initialization idempotent. Re-importing the package must not mutate global state unexpectedly or require additional configuration from users.

## Default library loading expectations
- Lazy backend probing is part of the user experience. Only adjust its order or side effects when the change has been reviewed for backward compatibility and documented for users.
- When adding, removing, or reordering backend candidates, make sure tests cover first-demand loading and the README in this directory is updated.
- Avoid importing optional heavy dependencies at module import time. All new optional integrations should use the same `configure.load_library` path.

## Top-level API stability
- Files `main.py`, `parse.py`, `kernel.py`, and the `configure` package form the primary public API that is re-exported from `pyunitwizard.__init__`.
- Do not rename or remove existing functions without deprecation shims.
- Keep function signatures backward compatible. Add new parameters as keyword-only when possible.
- Document any user-facing change in `pyunitwizard/pyunitwizard/README.md` and update tests to reflect the new behavior.

## Testing expectations
- Run the relevant pytest targets (at minimum `pytest tests`) after editing these modules.
- Add regression tests whenever you fix a bug or change default initialization.
