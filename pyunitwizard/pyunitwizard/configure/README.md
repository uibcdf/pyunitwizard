# Working on `pyunitwizard.configure`

This note explains how to extend the configuration layer that wires third-party
unit libraries into PyUnitWizard.

## Adding support for a new unit library
1. Register the backend in `pyunitwizard/configure/configure.py`:
   - Append the canonical name to the `libraries` list so discovery helpers
     expose it.
   - Append the same name to `parsers` if the backend can parse string input.
   - Update `_aux_dict_modules` when the importable top-level package differs
     from the canonical key.
2. Implement the translation hooks under `pyunitwizard/forms/` so
   `forms.load_library()` can adapt the library. Follow the patterns used for
   existing backends.
3. Add regression tests in `tests/` that exercise `configure.load_library()`
   with the new name. Ensure tests cover both eager initialization and explicit
   calls made by users.
4. Document the new backend in user-facing docs (Sphinx notebooks or README) to
   help consumers discover it.

## Customizing standard units
- Use `configure.set_standard_units()` in tests or examples to declare the
  canonical units for each dimensionality. The helper resets all internal
  dictionaries before applying new units, so pass the complete list of desired
  standards each time.
- When adding new derived quantities, update `kernel.order_fundamental_units`
  and expand the logic in `set_standard_units()` as needed to keep tentative
  base standards accurate.
- Maintain coverage by extending `tests/test_standardize.py` with new cases that
  assert conversions using the updated standards.

## Testing configuration changes
1. Always start tests with a clean kernel state by calling `configure.reset()`
   (or the `puw_kernel` fixture in `tests/helpers.py`). This mirrors the import
   behavior in `pyunitwizard.__init__`.
2. Run `pytest tests/test_configure.py` to cover `load_library`, defaults, and
   reset behavior whenever you touch configuration logic.
3. Execute the full suite with `pytest tests` before shipping changes that
   affect eager initialization to ensure downstream modules still behave as
   expected.
