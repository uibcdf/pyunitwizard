# Contributing Workflow

Use this flow for normal pull-request contributions. Authorized internal
direct pushes follow the
[common checkpoint policy](https://github.com/uibcdf/pyunitwizard/blob/main/MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints),
with scoped local validation, retained evidence and applicable head CI.

## 1. Prepare

- Sync `main`.
- Create a focused branch for one scope.
- Confirm local environment is up to date.
- Use the routine Python 3.14 workspace described in
  [Development Environment](development-environment.md).

## 2. Implement

- Keep changes atomic and reviewable.
- Update tests for behavior changes.
- Update docs for user-visible changes.

## 3. Validate

Run at least:

```bash
python -m pytest --receptor=llm tests
make -C docs html
```

## 4. Deliver

- Create coherent commits.
- Push branch.
- Open PR with clear scope, risk, and validation summary.
