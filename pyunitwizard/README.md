# PyUnitWizard package contributor guide

This document gives human contributors a tour of the public package layout and explains how to make changes safely.

## Package overview

Importing `pyunitwizard` triggers `pyunitwizard.__init__`, which:
1. Boots the runtime by calling `kernel.initialize()` to zero out all module-level state.
2. Eagerly probes for supported unit libraries (`pint`, `openmm.unit`, `unyt`, `astropy.units`) and loads each one that can be imported through `configure.load_library`.
3. Re-exports the user-facing helpers from `main.py`, plus configuration utilities from `configure`, so most consumers only need `import pyunitwizard as puw`.

Because initialization happens at import time, edits to any of the modules below must preserve idempotence and backward compatibility.

## Layout highlights

- `main.py` — Home of the top-level quantity/unit helpers (`convert`, `get_value`, `is_quantity`, etc.). This module delegates to the private form/parsing helpers and expects the kernel defaults to be ready. Touch this file when you add or modify high-level operations exposed to users.
- `parse.py` — Implements `parse()` and related helpers for string-to-quantity conversion. Use this module for parser-specific behavior. Keep changes in sync with the translation tables in `forms` when you add new representations.
- `kernel.py` — Defines `initialize()` and stores global registries (`loaded_libraries`, defaults, and dimensional standards). Only adjust it when you need to change how the runtime state is structured or reset.
- `configure/` — Hosts configuration utilities that manage the kernel (`load_library`, defaults setters/getters, standard unit helpers). Reach for this package when wiring new unit systems, customizing defaults, or resetting state for tests.
- Other packages:
  - `forms/` and `_private/` contain translation logic and implementation details used by the public modules.
  - `constants/` exposes physical constants and aliases.
  - `utils/` groups developer-facing helpers (I/O, conversions, and convenience routines).

Refer to `pyunitwizard/AGENTS.md` in the repository root for project-wide guidelines, and `pyunitwizard/pyunitwizard/AGENTS.md` in this directory for module-specific rules.

## When to edit each module

- Start in `main.py` if you are adding or adjusting APIs that users call directly. Keep signatures stable, introduce keyword-only parameters for new options, and backfill docstrings.
- Modify `configure/configure.py` when you need to change default library loading order, support a new library, or expose additional configuration helpers.
- Extend `parse.py` when parsing rules or grammar need to evolve. Add targeted tests that cover both string input and the resulting quantity form.
- Update `kernel.py` only when the core lifecycle or stored registries change. Ensure imports of `pyunitwizard` remain safe even if optional dependencies are missing.

## Testing expectations

- Run `pytest tests` after modifying any of the public modules above.
- Add regression tests for any change in default behavior (e.g., different default form, new eager-loaded library, new parsing branch).
- When adjusting import-time side effects, include tests that exercise a fresh interpreter state (for example by using `importlib.reload`).
- Document user-visible changes in this README and the repository-level changelog or release notes as appropriate.
