# Sphinx Documentation Workflow

PyUnitWizard documentation is built with Sphinx + MyST + myst-nb.

## Local build

```bash
make -C docs html
```

The generated site is written to `docs/_build/`.

## Contribution expectations

When you update behavior or public contracts:
- update the relevant User and/or Developer pages,
- ensure links and toctrees remain valid,
- keep narrative structure explicit (guided, not fragmentary).

## Common pitfalls

- orphan pages not included in any toctree,
- stale examples that no longer match runtime behavior,
- notebook content copied from unrelated projects.

Run documentation build locally before opening a PR.
