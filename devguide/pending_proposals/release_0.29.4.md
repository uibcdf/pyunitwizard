---
summary: Qualify and publish the 0.29.4 object-row capability maintenance release.
issue: uibcdf/pyunitwizard#150
status: active
opened: 2026-11-11
closed:
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
