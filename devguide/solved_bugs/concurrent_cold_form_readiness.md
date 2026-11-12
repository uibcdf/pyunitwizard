---
summary: Wait for cold backend and parser initialization before admitting concurrent readers.
issue: uibcdf/pyunitwizard#151
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: medium
verification: reproduced
area: [initialization, concurrency, parsing]
guard: tests/test_concurrent_first_use.py::test_concurrent_reader_waits_until_backend_and_parser_ready
normative:
blocked_by: []
supersedes: []
---

# Concurrent cold form readiness

OpenCASTp #13 reports two concurrent first quantity constructions, one failing
with LibraryWithoutParserError and the other returning the expected value.
The provider-only reproduction also fails on current clean main
064c7e1bca9333e2c7ebadccd7ec6fcf97d17046, Python 3.14.7. This establishes
source behavior, not separate qualification of the immutable public file.

The process-global `_LOADING` flag prevents recursive configuration but also
lets another thread pass before backend/parser registration completes. The
existing registry RLock protects registration, while this earlier admission
route bypasses it. A ready-library marker can also appear before the enclosing
configuration operation has selected its default parser.

Serialize cold admission with the existing reentrant registry lock and check
the recursion flag only under that lock. Readers must wait while initialization
is active, including after the backend is registered. Same-thread recursive
configuration must remain allowed. Keep the established warm path when no
initialization is active; no new backend, policy or public API is needed.

Fresh-process controls cover factory defaults, explicit Pint arguments,
configured defaults, OpenMM, unyt and Astropy; coordinated paused-loader cases
exercise both pre-registration and registered states. Retain caller policy,
optional-backend laziness, native failures and usability after failure.
Document ordinary public unit construction as optional serial preparation
before launching worker threads. This does not make policy writers thread-local
or qualify free-threaded Python, arbitrary external backend imports or processes.

## Resolution and executed scope

Cold admission reuses the registry RLock. The recursion flag is examined under
that lock, and an active initializer also blocks readers of an already
registered backend until its enclosing configuration is complete. The ordinary
ready/idle path keeps its existing fast admission; signatures and dependencies
are unchanged.

The original thirteen-case selection reproduced eleven failures and two
passing controls. The independent waiting-reader failure control also fails
with the original admission and passes after correction. The final fifteen
fresh-process cases cover seven natural first-use choices, six coordinated
pre/post-registration choices, recursive configuration after native failure,
and a waiting reader recovering after the first initializer fails. The actual
context case verifies restoration of caller policy.

The complete local suite passes 1,165 cases, with three executed skips and
five optional collection skips. The first full attempt was interrupted due to
the independent source-snapshot recursion in #153; it is not passing evidence.
The corrected snapshot fixture permits the complete run under the same nested
basetemp. Existing #70 concurrent-client controls, lazy import tests, Ruff,
documentation build and 23 dependency-route checks pass.

The selected guard forces both incomplete registration states and verifies
a second reader cannot return prematurely, then checks numerical output and
policy. All fifteen cases are mandatory in each future staged installed cell;
missing/skipped parameter scenarios are rejected by workflow controls.
Release #152 owns public qualification. MolSysSuite #193 owns advance impact
coordination; OpenCASTp #13 retains consumer scientific receiving.
