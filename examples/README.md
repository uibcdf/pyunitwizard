
# Examples

The `examples/` directory ships two miniature libraries that illustrate how
PyUnitWizard can be wired into external code bases. They are meant for
documentation and tutorials only; do not treat them as production-ready
packages.

## Library Overview

- `testlib/` – demonstrates a relative-import layout. Its `_pyunitwizard`
  module loads Pint and `openmm.unit`, `main.py` exposes `sum_quantities`,
  `get_form`, and `libraries_loaded`, and `box/` offers helper functions to
  inspect or change the active unit form.
- `testlib2/` – mirrors the same features using absolute imports to match the
  guidance in the docs’ PEP 8 discussion.

## Quick Start

1. Install PyUnitWizard in editable mode from the project root if you have not already:

   ```bash
   pip install --no-deps --editable .
   ```

2. Try the examples in a Python shell:

   ```python
   >>> import testlib, testlib2
   >>> testlib.libraries_loaded()
   ['pint', 'openmm.unit']
   >>> testlib.sum_quantities('2cm', '3cm')
   >>> testlib2.sum_quantities()
   ```

Both packages delegate unit handling to their `_pyunitwizard` helpers, so you can
experiment with changing the default form through
`testlib.box.set_default_form(...)` or `testlib2.box.set_default_form(...)`.

## Maintenance Notes

- The user guide notebook (`docs/content/user/In_Your_Library.ipynb`) reproduces
  these files verbatim. Whenever you modify filenames, imports, or function
  signatures, update the notebook so readers see accurate examples.
- Keep the examples lightweight—avoid adding third-party dependencies or heavy computations.
- Coordinate any change that alters the loaded unit libraries with the
  documentation team so the narrative continues to match the code.

Refer to examples/AGENTS.md for automation guidelines that apply to this directory.

