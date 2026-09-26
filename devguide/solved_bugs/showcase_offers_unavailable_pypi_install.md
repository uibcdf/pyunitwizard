---
summary: The showcase notebook offered a PyPI installation route that cannot resolve PyUnitWizard.
issue: uibcdf/pyunitwizard#76
status: resolved
opened: 2026-09-21
closed: 2026-09-26
severity: medium
verification: inspected
area: [documentation, installation]
guard:
normative: docs/content/about/installation.md
blocked_by: []
supersedes: []
---

# Showcase offers an unavailable PyPI installation

## What

The README, installation guide and quickstart had been corrected to direct
users to the `uibcdf` Conda channel. The showcase notebook still instructed
readers to run `pip install pyunitwizard pint openmm unyt astropy`, although
PyUnitWizard and its required suite dependencies are not published on PyPI.

## How

The notebook's setup cell now uses Conda with the `uibcdf` and `conda-forge`
channels, consistent with the installation guide. The notebook was executed
successfully after editing, and its execution timestamp was refreshed.

## Why

A tutorial that starts with an impossible install command fails before users
reach the examples. The installation guide is the durable source for the
supported distribution route.

## Acceptance criteria

- All four issue-reported entry points describe a viable installation route.
- The showcase notebook executes after the documentation change.

## Resolution

The showcase now matches `docs/content/about/installation.md`, which states
the Conda channel route and explains the source-install exception. A direct
inspection found no remaining `pip install pyunitwizard` instruction in the
four reported entry points. The edited notebook executed successfully.
