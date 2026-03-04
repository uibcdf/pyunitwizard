# Docs/API Alignment Evidence (`0.21.x`)

This note records the RC evidence that user documentation and API
documentation are aligned with shipped behavior.

## Validation date

- 2026-03-04

## What was verified

1. User-facing docs include the current backend/support scope:
- hard runtime dependency: `pint`,
- optional backends: `openmm.unit`, `unyt`, `astropy.units`, `physipy`,
  `quantities`,
- transparent integration coverage for NumPy/Pandas/Matplotlib.

2. API documentation index resolves and points to:
- users API (`docs/api/users/api_user.rst`),
- developers API (`docs/api/developers/api_developers.rst`).

3. Sphinx build succeeds with current sources and generated autosummary pages.

## Build command and result

Command:

```bash
make -C docs html
```

Result:
- build succeeded,
- HTML output generated in `docs/_build`.

## Evidence pointers

- `docs/content/user/index.md`
- `docs/content/user/library-integrators.md`
- `docs/content/user/numpy-pandas-matplotlib.md`
- `docs/api/index.md`
- `docs/api/users/api_user.rst`
- `docs/api/developers/api_developers.rst`

## Notes

- Autosummary artifacts generated during build are treated as build outputs and
  are not part of versioned source changes.
