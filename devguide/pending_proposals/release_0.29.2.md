---
summary: Qualify and publish the 0.29.2 maintenance release.
issue: uibcdf/pyunitwizard#145
status: active
opened: 2026-11-10
closed:
verification: measured
area: [release, packaging, documentation]
guard: tests/test_noarch_conda_publication.py::test_staged_profiles_require_runtime_regressions
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Release 0.29.2

## Scope

This patch includes the Pint inclusive-cutoff correction (#143), the
canonical cache initialization example (#144), low-cost filtered probes
(#141), and Pint string-unit construction (#142). The public dependency
requirements and platform/minor ranges remain the same. The prepared
[release notes](../release_0.29.2_notes.md) describe the conversion scope
and the measured performance limits.

## Qualification

The staged plan retains the 29 exact-source jobs and 30 installed cells
used for the previous maintenance release. Scientific boundary changes
require installed evidence before public promotion. Each installed cell
requires the #143 binary64 boundary tests, the #142 factory-count regression
and the #141 live DEBUG regression. The canonical guide example runs in
source CI. The workflow uses the existing recipe, dependency selections and
staging provenance.

The initial combined local run passes 1,055 tests on Python 3.14 with eight
recorded skips, including five optional module collections. All 71 selected
Pint 0.25 tests pass. The 81 scalar/array cases from MolSysMT and 108 native
contact decisions pass against the joint local source. These checks precede
the hosted qualification of the release candidate.

The preparation changes pass 113 focused tests, Ruff, the report index and
the Sphinx HTML build. The pinned shared checker verifies all 23 dependency
routes with declared and installed public bounds.

Record the selected source, exact native runs, staging producer, file
digest and installed results before publishing. Promote that file by its
digest. Independently verify public main/index records, a clean public
installation, served docs and source archival. Hand off the canonical
guide commit and digest through the MolSysSuite release notice. MolSysSuite
coordinates synchronization and receiving with consumer owners.
