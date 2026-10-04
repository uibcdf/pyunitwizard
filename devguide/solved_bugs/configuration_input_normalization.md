---
summary: Configuration normalization modifies caller inputs and policy before rejection.
issue: uibcdf/pyunitwizard#98
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [configure, integration]
guard: tests/test_configure.py
normative:
blocked_by: []
supersedes: []
---

# Configuration input normalization

## What

`load_library` assigns normalized aliases into the caller's sequence. Lists
are changed and tuples fail with `TypeError`, although tuples are accepted
by its documented boundary. `set_standard_units` resets standards and
provenance before rejecting an invalid container, discarding an active policy.

## How

Add regressions for list ownership, tuple loading, and preservation of policy
on container rejection. Use the public ArgDigest list coercer to normalize
accepted containers before changing configuration state. Preserve existing
accepted types, exception classes, backend order, and physical unit checks.

## Why

Configuration accepts caller-owned data. Ordinary container normalization
must finish before state changes, and must not overwrite those inputs.
This is also the concrete runtime boundary reviewed under
`uibcdf/pyunitwizard#89`; the shared policy belongs to `uibcdf/molsyssuite#6`.

## Scope and exclusions

This does not promise transactionality for physically invalid unit strings
or change backend availability, parsing, dimensionality, or record integrity.

## Acceptance criteria

- Caller lists remain unchanged and tuples load in their original order.
- Invalid standard containers retain the previous policy and cached matrices.
- Scalar and unsupported iterable rejection keeps its established exception type.

## Measured regression and correction — 2026-10-04

Before implementation, both ownership/tuple cases and the rejected
`set_standard_units` policy case failed. The companion receiving tests also
exposed five ArgDigest 0.13 incompatibilities. After normalizing through
published ArgDigest 0.14, all 52 configuration/ecosystem tests passed.
The accepted-container checks retain their original exception types; the
provider performs the shared normalization rather than a local coercer copy.

The complete local Python 3.14 suite passed 688 tests with 20 documented skips.
Ruff check/format, reporting/dependency contracts, and the documentation build
passed. The tests in the named guard assert input preservation, tuple loading,
and unchanged policy/provenance/cache identity after invalid-container rejection.
