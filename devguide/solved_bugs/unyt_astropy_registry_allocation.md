---
summary: Reuse the shared Pint registry in unyt-to-Astropy translation.
issue: uibcdf/pyunitwizard#122
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: measured
area: [forms, performance]
guard: tests/forms/test_api_unyt.py::test_unyt_to_astropy_does_not_construct_a_registry_per_conversion
normative:
blocked_by: []
supersedes: []
---

# Repeated Pint registry construction in unyt-to-Astropy

## What

At source 0734c1467c0d747eccf19bd7bd6a19f548ab1e32, the unyt-to-Astropy
adapter calls `quantity.to_pint()` without a registry. Actual unyt 3.1.0 then
constructs a Pint UnitRegistry for every call. This dominates warmed coordinate
conversion and creates a false appearance of an intrinsic record-hub advantage
in #106's evaluation. No numeric defect is established here.

## How

Reuse the existing `quantity_to_pint(quantity)` helper, which supplies the shared
kernel registry, then the existing Pint-to-Astropy translator. No new cache,
definition table, record format, dependency or dispatcher is needed. Regression
tests set up the backends, forbid further Pint registry construction and verify
two repeated array conversions, length/velocity factors and float32 preservation.

## Why and evidence

Sequential local seven-repeat evidence on the retained 72×3 TopoMT coordinates:
direct median 275672.62 µs; freshly sealed record route 540.44 µs with telemetry
enabled. The tiled synthetic array gives direct 225394.40 µs and record 7143.33 µs.
These are source-checkout measurements on one host, not portable performance
promises or installed package qualification. Raw samples and hashes belong in
#106's retained before/after receipt. A live via-Pint control isolates the record
cost from shared-registry reuse.

## Acceptance criteria and limitations

- Allocation regression fails before the fix and passes afterward without a timing threshold.
- Numeric/dtype/shape and existing backend conversion tests pass.
- Remeasure all routes in both telemetry modes and retain original before source identity.
- Central pre-rollout notice: uibcdf/molsyssuite#127. Actual client use is unknown;
  source adoption and public installed artifact qualification remain separate.

## Resolution and executed checks

The adapter now calls its existing `quantity_to_pint` helper. Both allocation
regressions failed before the fix and pass afterward; they forbid the actual
registry constructor and check repeated length/velocity conversions with float32
values. This protects the allocation mechanism without a noisy speed threshold.
The legacy adapter tests now import the adapter explicitly for isolated execution.

The focused record/foreign-registry/backend/benchmark selection passes 108 tests
with one expected JSON/NaN skip. The complete Python 3.14.7 local suite passes
859 tests with that same one skip and one existing deprecation warning. It uses
the task-local physipy/quantities overlay documented in #120 and network access
for the isolated installed-consumer build, leaving the shared environment intact.
Repository-wide Ruff lint/format passes (213 files). The isolated owned-copy
Sphinx build passes without warnings. #106 retains before/after raw samples and
source identities; final exact-head CI evidence belongs in the issue closeout.
