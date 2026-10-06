---
summary: Complete distribution adoption using the general shared route contract.
issue: uibcdf/pyunitwizard#114
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: measured
area: [governance, distribution, compatibility]
guard: tests/test_dependency_routes.py
normative:
blocked_by: []
supersedes: []
---

# General distribution contract adoption

## What

Protect future dependency/installation-route changes with a maintained preflight,
retaining the qualified public Conda 0.28.1 artifact from uibcdf/pyunitwizard#112.
This administrative review adds no PyPI, Windows or API-stability claim.

## How

Reuse MolSysSuite provider `20628bd5dba6d759669b0d444fe657eb1edad33f` and its
general `molsyssuite.dependency-routes@2` contract, with 364 native governance
tests and 74 focused local tests under uibcdf/molsyssuite#45. The member owns its
inventory/thin invocation; parsing, comparison, recipe checks and native gate
verification remain provider-owned.

The inventory covers one local noarch recipe, nine environments (seven runtime,
two bootstrap-only) and twelve workflows. Production preserves the public
closure; development/test/documentation/optional-runtime environments may narrow
compatible release ranges with a reason. ArgDigest/Pint/OpenFF/interpreter
conditions remain unchanged. Conda selector/build semantics are retained. Parser
dependencies are developer tools, excluded from public runtime/production metadata.

Source jobs invoke actual-installed public-bound checks before tests or builds
within their existing jobs. Routine CI remains Linux/Python 3.14; science
selections, nightly debt and full/release matrices retain separate triggers.
Optional public source workflows explicitly select strict priority. Exact
installed staging retains its reviewed flexible-priority/archive/public-provider
provenance controls.

Before building, the publisher reviews declarations and reuses shared
`acquire_gates` to verify the five original source workflows, the exact candidate
and 29 executed job/step profiles. Required science/build jobs must execute the
default installed check. Backlog-only or skipped matrices cannot qualify through
aggregate green conclusions. Bootstrap does not install scientific runtime to
repeat already qualified source gates. A separate candidate receipt retains the
proofs; local release/version/resource/file/public-poststate controls remain.

## Why

The archived one-time receipt did not guard later drift. Exact text comparisons
also rejected justified test conditions. General comparison by route purpose and
actual installed bounds protects future candidates without a local engine copy.

## What is measured and what is assumed

Original clean owner snapshot: `2ab37a525ce99728ad8aee846b4a4f7acc4f1b65`.
All eight original recipe/runtime hashes matched the 0.28.1 receipt before this
integration. Six tool environments now declare parser dependencies; workflow
edits renew reviewed hashes. Original source/file/installed evidence is preserved.

The isolated 22-route prototype passes declaration and actual public-bound review
on Python 3.14.7 in `molsyssuite@uibcdf_3.14`, with both receptor imports from the
eligible primary local clones. Seven independent shared-workspace closure
findings remain uibcdf/molsyssuite#82 debt. This is not clean-solver, scientific or
exact-file qualification. Forty focused owner tests pass on the same interpreter:
`tests/test_dependency_routes.py`, `tests/test_noarch_conda_publication.py`,
`tests/test_conda_release_route.py` and `tests/test_reporting_protocol.py`, using
`pytest --receptor=llm`. Ruff 0.16.5, the shared repository-conformance check,
generated indexes and whitespace checks pass. The integrated default invocation
verifies all 22 routes and actual installed public bounds. Owner native CI/final
identities are verified below.

### Hosted qualification and resolution

Implementation **d128b37b4339d3b8520678cc9d8924f902d14a7b** is published
on main. GH Run Receptor full native captures independently confirm ordinary CI
[37497852682](https://github.com/uibcdf/pyunitwizard/actions/runs/37497852682)
and common policy
[37497853464](https://github.com/uibcdf/pyunitwizard/actions/runs/37497853464)
complete successfully at that exact source. Logs demonstrate the default
22-route installed-bounds audit, source checks and existing suite selection:
**785 passed / 19 skipped** on Linux/Python 3.14. The skip count remains visible;
this is not a new full cross-platform or optional-backend qualification. Coverage
upload is queued successfully; downstream processing is a separate observation.
The policy executes repository conformance, lint/import and formatting checks.
This meets the owner adoption acceptance criteria; future candidates retain
independent full source, installed-file and promotion gates.

This report is archived with its maintained guard module. The original release
receipt remains unchanged; central adoption records reference this source review
and the original public artifact separately.

## What was refuted

- Rewriting backend conditions to fit exact string comparisons.
- Replacing a qualified local publisher to match another plan schema.
- Equating release-range proof with installed-version evidence.
- Equating aggregate success with executed required source jobs.
- Rebuilding 0.28.1 to complete governance adoption.

## Scope and exclusions

Conda source/distribution controls only. Preserve scientific code, public
metadata/version/tag, original archive/producer/qualification/promotion, external
pins, optional API decisions and ordinary test selections. No publication is
triggered by this work.

## Acceptance criteria

- All 22 routes are reviewed; default invocation checks actual public bounds and
  preserves failure exit statuses.
- Provider guards reject missing recipe requirements, weak runtime floors/
  ceilings, below-floor sources and unsupported/unsafe ranges. Local guards
  protect the immutable pin, default source invocation, exact candidate binding,
  complete 29-job native profile, prepublication ordering and science conditions.
- Applicable source CI demonstrates the executed audit and governance controls.
  Full candidate matrices remain future release evidence; do not dispatch them
  for this source-control review.
- Retain version/resource/immutable-coordinate/public-poststate guards and the
  original independently verified public file evidence.
- Archive/synchronize this owner record before registering central adoption with
  source and public evidence kept distinct.

## Dependencies and risks

Unknown syntax needs provider review; it cannot weaken public requirements.
Workflow hashes need manual review after edits. Scientific failures remain owner
work and may block a future publication independently of this adoption.

## Guard relevance

`tests/test_dependency_routes.py` exercises provider identity/tamper, native job
profile completeness, offline-qualification misuse, candidate source binding,
publication ordering and preservation of science constraints. Provider engine
negatives remain maintained in MolSysSuite, with exact immutable source identity.
