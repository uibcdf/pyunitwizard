---
summary: Reuse the shared registry in remaining unyt dimensionality and OpenMM paths.
issue: uibcdf/pyunitwizard#123
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [forms, performance]
guard: tests/forms/test_api_unyt.py
normative:
blocked_by: []
supersedes: []
---

# Remaining unyt registry allocations

## What

After #122 fixed the Astropy path, `api_unyt.dimensionality` and
`quantity_to_openmm_unit` still call unyt's `to_pint()` without a registry.
Actual unyt 3.1.0 constructs a fresh Pint UnitRegistry when it is omitted.
At base 96da2c742fe6851c8270ac88682c58751baf39bc, constructor counting gives
two allocations for two direct adapter dimensionality calls, one for two public
dimensionality queries (the second is cached), and two for two public OpenMM
conversions. Numerical values remain correct; no numerical defect is asserted.

## How

Reuse the existing owner operation `api_unyt.quantity_to_pint`, which supplies
the kernel's shared registry. Unit-only OpenMM translation already delegates
through quantity translation. No new cache, unit table, format, API, dependency
or global policy is required. Keep #122's bounded historical result unchanged.

## Why

Uncached dimensionality queries and repeated live translation should not pay
registry construction costs. The existing public cache bounds some queries,
so tests exercise the adapter as well as public calls and do not claim every
public dimensionality query allocates.

## Acceptance criteria

- Regression-first tests forbid actual Pint registry construction after backend setup.
- Quantity/unit dimensionality and repeated array/unit OpenMM translation preserve
  factors, dimensions, float32/float64 dtype, shape and the molecular mass policy.
- Relevant and full local tests, Ruff, docs and final exact-head native gates pass.
- Retain source adoption and public artifact identity separately; no 0.28.2 release here.

## Dependencies and scope

Pre-rollout provider notice: uibcdf/molsyssuite#127, including the #123 candidate
notice from the preceding review. Actual client use remains an owner question.
Source qualification does not establish a replacement public artifact, a complete
optional-provider matrix or adoption in other clients. Existing shared environment
gaps remain with uibcdf/molsyssuite#82.

## Resolution and evidence

Both calls now use `quantity_to_pint`, the existing helper supplying the shared
registry. The dimensionality docstring names its actual unyt input types.
Parser flags, dispatch keys, public signatures, dependencies and the existing
public cache are unchanged. The unit translator continues to delegate through
the quantity translator. No argument-free `.to_pint()` call remains in the
package source inspected for this task.

Fifteen native-unyt-input regressions fail before the fix and pass afterward:
six quantity/unit dimensionality cases, six repeated 2-D array conversion cases
(float32/float64), and three direct/public unit conversion cases. They forbid
actual registry construction after backend setup, rather than using timing
thresholds. They check angstrom/nanometer factors, compound velocity dimensions,
shape/dtype, and native unyt amu→OpenMM dalton→Pint pure-mass round trips. The
module guard addresses both affected operations and the existing Astropy guard.

The initial fixture batch also encountered five unrelated input-construction
failures: Pint `dalton` cannot enter unyt. That is separately owned by #124.
Switching these fixtures to actual native unyt `amu` quantities/units isolates
#123's mechanism; the corrected before batch then fails all fifteen tests for
the intended allocation reason. No dalton-construction fix is claimed here.

Constructor counts for the same two-call angstrom workload:

| Operation | Before | After |
|---|---:|---:|
| Direct unyt dimensionality adapter | 2 | 0 |
| Public dimensionality, including one cache hit | 1 | 0 |
| Public unyt→OpenMM, requested nanometers | 2 | 0 |

Public conversion values remain `[0.1, 0.2] nm`. The measured reduction concerns
registry allocations; no portable wall-time speedup is asserted.

## Validation and closeout

Local Python 3.14.7 / Pint 0.25.3 / unyt 3.1.0 / OpenMM 8.6.1:

- 66 focused unyt/OpenMM/backend/benchmark tests pass.
- Complete local suite: 875 passed, one expected strict-JSON/NaN skip and one
  existing `pyunitwizard.main` deprecation warning.
- As in the prior source qualification, missing physipy 0.2.8 and quantities
  0.16.4 are installed only in the task-owned temporary overlay. The isolated
  installed-consumer test has network access; the shared environment is unchanged.
- Repository-wide Ruff lint/format passes (214 files); the owned-copy Sphinx
  build passes with zero warnings. Report indexes and diff checks pass.

Final unskipped exact-head native CI/policy receipts belong in the owning issue
closeout. Provider notice was delivered before the push through MolSysSuite #127;
its consumer adoption remains independently owned. Original public 0.28.1
artifacts keep their source/file identities. No 0.28.2 tag, package or new public
qualification is created by this source correction.

The next bounded patch candidate is #124's independently reproduced atomic-mass
translation failure. No speculative backend, storage layout or append feature
is added by this work.
