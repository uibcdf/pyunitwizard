# Naming Conventions

Clear naming is a core maintainability requirement for PyUnitWizard.

## Repository and package

- Repository name: `pyunitwizard`
- Import package: `pyunitwizard`
- Conda environment names: choose explicit lowercase identifiers, for example `pyunitwizard-dev`.

## Python code conventions

Follow PEP 8 conventions consistently:
- modules/functions/variables: `snake_case`,
- classes/exceptions: `PascalCase`,
- constants: `UPPER_CASE`,
- internal-only symbols: single leading underscore (`_name`).

## API naming guidance

Prefer names that describe behavior, not implementation details.

Good examples in this project:
- `are_compatible`, `get_dimensionality`, `set_standard_units`

When adding new public symbols, keep naming aligned with existing API families
so user-facing behavior remains predictable.
