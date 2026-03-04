# Docstring Standards

PyUnitWizard uses NumPy-style docstrings for contributor-facing consistency.

## Scope

Use complete docstrings for public functions, methods, and classes.
At minimum, include:
- short summary,
- parameters,
- returns,
- raised errors when relevant,
- examples for behavior-sensitive API paths.

## Style guidance

- Keep summaries short and explicit.
- Document units expectations when behavior depends on dimensionality.
- Prefer examples that match real API usage in this repository.

## Validation

When adding or changing public API behavior, verify that docstrings and user
docs describe the same contract.
