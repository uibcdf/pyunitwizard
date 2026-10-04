---
summary: Full-suite release and development profiles omit supported backends.
issue: uibcdf/pyunitwizard#99
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [testing, release, dependencies]
guard: tests/test_lazy_backend_loading.py::test_explicit_loading_imports_only_the_requested_optional_backend
normative:
blocked_by: []
supersedes: []
---

# Full-suite profiles missing supported backends

## What

Release Gates `37230869147` at scientific source
`1a10ae9cca56b5766d09426e9964687771b6cb2a` failed all four Python
3.11–3.14 full-suite jobs. Each job passed the API/ecosystem smoke, but
six full-suite tests failed because `physipy` and `quantities` were absent.
The packaging and documentation jobs passed. The full matrix supplies
both dependencies; the release and development profiles omitted them.

## How

Add the same pip backend dependency entries already used by `test_env.yaml`
to the release and development profiles. Keep scientific and lazy-loading
assertions enabled. Run Release Gates at the corrected exact source.

## Why

Both profiles run the maintained scientific suite, which exercises every
supported adapter. Omitting providers makes gate outcomes depend on the
chosen profile instead of the tested implementation.

## Scope and exclusions

These are test/development dependencies. The production dependency boundary
and public scientific behavior are unchanged. Optional attribution provider
coverage remains a separately documented scope.

## Acceptance criteria

- Both full-suite profiles supply all six supported unit adapters.
- All four release full-suite jobs actually execute and pass.
- Existing lazy-load tests prove that importing the package does not import
  optional providers and requesting one imports only that adapter.

## Verification

The failure was measured before the environment change, with 6 failures,
650 passes, and 29 skips in the Python 3.14 full-suite job. The isolated
full-backend local suite passed 688 tests with 20 documented skips before
this profile correction; its dependency closure is the intended local model.
Hosted recovery passed in Release Gates `37231437144` at
`bd5be9e4853a3b3a8783618463ae3d641613f6c8`: all four Python 3.11–3.14
jobs executed both smoke (16 passes) and full suite (686 passes, 22 documented
skips); packaging and documentation jobs also passed. Routine CI
`37231386080` and policy `37231386414` passed at the same head.
The named guard executes a fresh-process load for each supported optional
adapter, so missing providers fail at the actual operation boundary.
