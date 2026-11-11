---
summary: Qualify and publish the 0.29.4 object-row capability maintenance release.
issue: uibcdf/pyunitwizard#150
status: resolved
opened: 2026-11-11
closed: 2026-11-11
verification: measured
area: [release, packaging, provenance]
guard: tests/test_noarch_conda_publication.py::test_staged_profiles_require_runtime_regressions
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Release 0.29.4

The maintainer requests #148 resolution, remaining-issue triage and a new
publication. The provider documents numeric object-row capabilities and
ownership and exposes a specific TypeError subtype for unsupported Astropy
construction/translation and native unyt conversion. The advance consumer
notice is [MolSysSuite #186](https://github.com/uibcdf/molsyssuite/issues/186).
MolSysMT #693 retains consumer scientific ownership.

The exact-source plan retains all 29 source jobs and all 30 installed cells.
Every installed cell must execute row construction, scaling, translation
and both unsupported-backend diagnostics, plus prior runtime regressions.
The optional OpenFF profile must also execute its object-row guard. Synthetic
JUnit controls reject absent or skipped required regressions. The package
is built once into staging, inspected, qualified and promoted by digest.
Public label/index, clean installed receiving, documentation and source
archival will be checked independently before closeout.

The open-issue audit finds no open PR. #44 and #52 lack a concrete consumer
contract; the bounded package-source inspection of MolSysMT, MolSysViewer
and Sabueso finds neither integration. #87's inert-form consumer prerequisite
is met, but no measured material record/backend cost or conversion-unpreventable
scientific error has been supplied. #148's existing backend representation
restriction can be documented and diagnosed without a new computing class.
The three conditional proposals remain open for their stated triggers.

Local qualification passes 1,149 tests, with three executed skips (two Zarr,
one strict JSON NaN) and five optional collection skips. The documentation
build, Ruff and all 23 pinned dependency-route checks pass. The initial
full-suite run exposed global policy leakage in the new tests; a module-local
context fixture restores caller policy and the complete suite then passes.
No runtime concentration aliases or application policy were changed.

## Verified publication outcome

The stable tag and [GitHub Release 0.29.4](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.4)
identify original source `d9dd0261d7e1f43624f4dd9356830ab9b126bd14`.
All 29 required exact-source jobs passed. Producer 42976420354/1 built
`pyunitwizard-0.29.4-py_0.tar.bz2`, 98,914 bytes, SHA-256
`72dfeb00132ec851b1913d4b5ceabb9426d835c7556d8ad227e9bd6723d170f9`.
The archive's 94 tracked Python sources, resource bytes, licenses and
metadata match the candidate.

Installed qualification 42977025610/1 passed all 30 cells, with 14,276
passing entries and 164 expected skips: 110 older Ackredit prepared API,
30 strict JSON NaN and 24 OpenFF cases outside the OpenFF profile. All
required guards execute, including 24 buffer/policy, eight scaling, four
Astropy diagnostic, three unyt diagnostic, twelve Astropy translation and
nine compatible-translation cases per cell. All six OpenFF cells execute
their optional row case. Native source/run/attempt, archive digest, public
provider floors and complete dependency closures were checked independently.

Promotion 42977978865/1 preserves the qualified digest. Independent
anonymous public main-label and solver-index verification passes. The release
event's publisher passes its staged decision and skips both build steps.
A fresh public-only Linux/Python 3.14 receiving prefix passes 126 tests
and pip check outside the checkout, with no skipped test. One optional
OpenFF case is explicitly deselected; its qualification is in the six
installed matrix cells. Actual SDK `95f693be10c9205ab9b912cb53453710a207bf45`
accepts cold/application-policy imports and rejects outside-prefix, symlink
and source-checkout controls in both scenarios.

Canonical guide commit `46e5927a551315582ce43faa527b7c0d67d45cf9`, digest
`3068a9b7c5b868e8ae4c3e48f487119021df971f0d3f2293e6cae85ac7d410ac`,
is published and delivered through [MolSysSuite #187](https://github.com/uibcdf/molsyssuite/issues/187).
The suite owns client synchronization; MolSysMT #693 owns scientific receiving.
Documentation build 42978469371 and Pages deployment 42978585325 pass.
The actual installation, compatibility and backend pages serve 0.29.4
and the reviewed contract over their canonical public URLs.

Zenodo verifies the source snapshot under version DOI
[10.5281/zenodo.24128389](https://doi.org/10.5281/zenodo.24128389).
This does not claim archival of the Conda file.

The publication evidence is retained in
[evidence/release_0.29.4_publication.json](../evidence/release_0.29.4_publication.json),
alongside the exact-source proof, installed proof and complete resolved closures.
The installed-workflow guard protects against absent or skipped runtime
regressions in a future staged publication; the receipts establish the actual
executed scope of this version. No new actionable issue or open PR was
found at the pre-publication audit. #44, #52 and #87 remain conditional.
