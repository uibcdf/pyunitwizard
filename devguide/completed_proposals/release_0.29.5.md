---
summary: Qualify and publish the 0.29.5 concurrent initialization maintenance release.
issue: uibcdf/pyunitwizard#152
status: resolved
opened: 2026-11-12
closed: 2026-11-12
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

## Verified publication outcome

Stable [GitHub Release 0.29.5](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.5)
and its annotated tag identify original source `1783fab011a99567f26e988479ee7dd74c494c6f`.
All 29 exact-source jobs passed. Producer 43176456805/1 built
`pyunitwizard-0.29.5-py_0.tar.bz2`, 98,829 bytes, SHA-256
`4f348207721f7f57400d697506c9149e9a6733e4ff010ce82b915731b00ecac7`. The archive's 94 tracked Python
sources, resource bytes, metadata and licenses match the candidate.

Installed qualification 43177365172/1 passes all 30 Linux/macOS arm64
cells on Python 3.11–3.14 (OpenFF 3.12–3.14), with 14,726 passing entries.
All fifteen new fresh-process cases execute in every cell: seven natural
first-use choices, six coordinated readiness choices, recursive configuration
and waiting-reader recovery. Prior required guards also execute. The 164
expected skips are older Ackredit prepared API (110), strict JSON NaN (30)
and OpenFF outside its optional profile (24). Dependency closures and native
source/run/attempt, required steps and exact digest were audited independently.

Promotion 43178501834/1 preserves the qualified digest. The release event
passes its staged decision and skips both build steps. Independent anonymous
public main-label and solver-index verification passes. A clean public-only
Linux/Python 3.14 receiving environment passes 141 tests and pip check outside
the checkout, with no skipped case. One optional OpenFF case is explicitly
deselected; its six matrix cells provide that qualification. Actual SDK
`95f693be10c9205ab9b912cb53453710a207bf45` accepts installed imports under
cold/application-policy scenarios and rejects outside-prefix, symlink and
source-checkout controls in both.

Canonical guide commit `7bac29f97d17403453c30bfa02c1e2ecb4653b77`, SHA-256
`2bebdab26b9f5ac70bafd35bc48522e1a07535953e2a1b8939e0a3feb6d5b860`, is published before
[MolSysSuite #194](https://github.com/uibcdf/molsyssuite/issues/194)
receives its exact identity. MolSysSuite owns client synchronization and
OpenCASTp #13 owns independent scientific receiving. Documentation build
43179970055 and Pages deployment 43180091781 pass. Actual
installation, compatibility and backend pages return HTTP 200, identify
0.29.5 and serve the reviewed initialization contract. Source archival is
verified under [version DOI 10.5281/zenodo.24154809](https://doi.org/10.5281/zenodo.24154809); Conda-file
archival is not claimed.

## Source integration and completeness

Upstream advanced with a governance-only instruction during local work. The
first push was rejected; four accidentally dispatched prior-remote-head runs
were withdrawn, and premature issue-closeout comments were corrected. The
remote update was preserved in a merge, then the successful push was verified.
Every accepted source gate and the original producer/installed workflow bind
to the final candidate above. The excluded runs and actual native identities
are retained separately in the publication receipt; they do not qualify it.

The complete owner inventory traverses two issue pages, filters PR entries
and retains 99 issue records. A separately complete open-pull traversal has
zero records. Before publication, only this release and conditional proposals
#44, #52 and #87 remain open. The bounded acquisition summaries and hashes,
source proof, installed proof, resolved closures and public receiving/docs/
archival results are retained in `devguide/evidence/release_0.29.5_*.json`.
The installed-workflow guard and missing/skipped parameter controls protect
future publication coverage; the receipts establish this version's execution.
