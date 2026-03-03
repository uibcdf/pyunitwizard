# Contributor Checklist

Use this checklist before opening a PR or preparing a release commit.

## Code and behavior

- [ ] Public behavior change is covered by tests.
- [ ] No undocumented contract changes.
- [ ] Runtime configuration behavior remains deterministic.

## Diagnostics

- [ ] SMonitor-related behavior is documented when changed.
- [ ] No hardcoded diagnostics bypass catalog-driven patterns.

## Documentation

- [ ] User docs updated for integration-facing changes.
- [ ] Developer docs updated for contributor-facing changes.
- [ ] `devguide/` remains aligned with docs changes.

## Validation

- [ ] `pytest -q` passes.
- [ ] `make -C docs html` passes.
- [ ] Changes are committed in focused, coherent commits.
