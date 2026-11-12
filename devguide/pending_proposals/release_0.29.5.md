---
summary: Qualify and publish the 0.29.5 concurrent initialization maintenance release.
issue: uibcdf/pyunitwizard#152
status: active
opened: 2026-11-12
closed:
verification: measured
area: [release, packaging, provenance]
guard: tests/test_noarch_conda_publication.py::test_staged_profiles_require_runtime_regressions
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Release 0.29.5

The maintainer requests #151 resolution and a new publication. Source fix
3262b19dce5bad12f7abeff67cd3574de547a7f2 reuses the registry RLock at cold
form admission. Readers wait for backend/parser readiness; recursive
configuration, idle warm admission, caller policy and native failures remain.
OpenCASTp #13 owns scientific receiving; MolSysSuite #193 carries advance
provider-impact notice. No dependency floor or public API is added.

The complete local runtime/source suite passes 1,165 tests, with three
executed skips and five optional collection skips. Fifteen new fresh-process
cases cover seven natural choices, six coordinated pre/post-registration
choices, recursive configuration/failure cleanup and waiting-reader recovery.
Documentation, Ruff and 23 pinned dependency-route checks pass. The original
13-case control has eleven failures; the additional waiting-failure control
also fails with original admission. The corrected guards pass.

The first full run was interrupted at 386.98 seconds with 1,148 passing
cases and three executed skips; that incomplete run does not qualify. #153
corrects the separate installed-consumer fixture's recursive checkout copy
when basetemp is nested in ignored tooling. A finite Git-selected snapshot
preserves current/new source and excludes ignored tooling/private material.
The bounded guard and complete same-basetemp suite pass afterward.

The final release plan retains 29 exact-source jobs and 30 installed cells,
one archive built into staging and promoted by digest. Each installed cell
must execute all fifteen cold-admission cases. Synthetic JUnit controls reject
missing/skipped individual cases. Prior row/origin/cutoff/calorie/profile guards
remain mandatory. Public main/index, clean public receiving, served pages,
source archival and canonical-guide delivery will be verified separately.
