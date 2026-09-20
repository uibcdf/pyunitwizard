---
summary: Decide whether forallpeople should become a supported quantity form.
issue: uibcdf/pyunitwizard#44
status: open
opened: 2026-09-19
closed:
verification: inspected
area: [integration, forms, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Decide whether forallpeople should become a supported quantity form

## What

Evaluate `forallpeople` as a possible optional PyUnitWizard quantity form after 1.0. The
project is active, published version 3.0.0 on 2026-08-22, and represents immutable
`Physical` values in SI base units with dimension vectors and environment-dependent
display factors.

## How

Do not add a dependency or backend from package popularity alone. Begin with a real
MolSysSuite or external workflow that must exchange a `forallpeople.Physical` object with
one of PyUnitWizard's existing forms. A future spike must define detection, value and unit
extraction, dimensionality, construction, conversion in both directions, arrays,
dimensionless results, optional-dependency behavior and environment isolation.

## Why

The model is technically plausible but not automatically equivalent to the existing
backends. `forallpeople` stores magnitudes in SI base units, can return plain numbers when
dimensions cancel, and changes representation through a loaded environment. Those
semantics touch PyUnitWizard's conversion and shared-policy boundaries. No current issue
or measured consumer demonstrates that the maintenance cost is needed for stabilization.

## Evidence

The 2026-09-19 review used the upstream 3.0.0 release metadata, current README and
`pyproject.toml`. The upstream project is active and Apache-2.0 licensed. This establishes
viability for a later experiment, not demand or compatibility.

## Scope

This is post-1.0 and does not block the stabilization wave. `forallpeople` would remain
an optional dependency. Supporting it must not mutate a user's loaded environment or
make environment selection part of PyUnitWizard's process-global unit policy.

## Acceptance criteria

1. A concrete user or MolSysSuite workflow requires object-level interoperability.
2. A compatibility matrix states the behavior for quantities, units, arrays,
   dimensionality, dimensionless results and environment-dependent representation.
3. Round-trip tests cover at least one existing backend in both directions.
4. Python 3.11--3.13 support and optional installation are demonstrated.
5. Maintainers accept the ongoing backend and upstream-version support cost.
6. The proposal is then accepted for implementation or closed as unnecessary.

## Recommendation

Defer implementation until after 1.0 and until criterion 1 exists. The current evidence
supports removing `needs-triage`; it does not support adding `forallpeople` now.
