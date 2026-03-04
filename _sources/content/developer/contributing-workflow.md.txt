# Contributing Workflow

Use this flow for all documentation and code contributions.

## 1. Prepare

- Sync `main`.
- Create a focused branch for one scope.
- Confirm local environment is up to date.

## 2. Implement

- Keep changes atomic and reviewable.
- Update tests for behavior changes.
- Update docs for user-visible changes.

## 3. Validate

Run at least:

```bash
pytest -q
make -C docs html
```

## 4. Deliver

- Create coherent commits.
- Push branch.
- Open PR with clear scope, risk, and validation summary.
