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

- [ ] `python -m pytest --receptor=llm tests` passes for a PR or release;
  authorized internal direct pushes record checks selected under the
  [common checkpoint policy](https://github.com/uibcdf/pyunitwizard/blob/main/MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints).
- [ ] `make -C docs html` passes.
- [ ] Changes are committed in focused, coherent commits.
