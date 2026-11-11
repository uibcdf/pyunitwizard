---
summary: Qualify and publish the 0.29.2 maintenance release.
issue: uibcdf/pyunitwizard#145
status: resolved
opened: 2026-11-10
closed: 2026-11-11
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

The first candidate, `30325ca605a8d1eadd5433f0417923496a32d6e8`, failed hosted
source tests because the synthetic installed JUnit sample contained only
calorie cases. The new runtime assertions require the additional cases.
The corrected sample exercises both the pass path and each missing or
skipped required case. The installed workflow and release gates are unchanged.
[Failed Release Gates run](https://github.com/uibcdf/pyunitwizard/actions/runs/42936793408)

A local twelve-worker run also reproduced an order-dependent affine append
test. The test constructs Pint quantities using Pint's `degC` spelling.
It now selects the Pint parser explicitly, including when a previous test
has selected Astropy. The full corrected local run passes 1,062 tests with
the same eight recorded skips. The production append implementation is
unchanged.

## Publication outcome

The stable tag and GitHub Release `0.29.2` identify
`cf40c9fcdd4cd2d18df78a9d8fcef3b2d9516256`. All 29 source jobs and ordinary
CI passed. The staging producer built one noarch file.
[GitHub Release](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.2)

The 30 installed cells passed with 12,140 passing entries and 140 expected
skips for strict JSON NaN and the older Ackredit prepared API. Each cell
executed all 27 boundary cases, the fresh-object construction regression and
the live-level diagnostic regression. Promotion reused the 98,016-byte file
with SHA-256 `bb28b9420760b557025163e11c934e096c7b98200cac720100a2db924e9ee617`.
Public label and solver-index verification passed. A new public-only Linux
Python 3.14.10 environment passed 35 tests and `pip check`.
[Installed run](https://github.com/uibcdf/pyunitwizard/actions/runs/42939335711) ·
[Promotion run](https://github.com/uibcdf/pyunitwizard/actions/runs/42940169699)

The documentation build and Pages deployment passed. The public
installation, compatibility and backend coverage pages serve 0.29.2 and
the updated dependency and conversion guidance.
[Pages deployment](https://github.com/uibcdf/pyunitwizard/actions/runs/42940959172)

The canonical guide was published at `30cfdba879ea651d86ecac187536a32ab3f01978`.
MolSysSuite received the exact revision and digest for its client
synchronization. The source snapshot is verified on Zenodo.
[MolSysSuite notice](https://github.com/uibcdf/molsyssuite/issues/180) ·
[Zenodo version DOI](https://doi.org/10.5281/zenodo.24122890)

The [publication receipt](../evidence/release_0.29.2_publication.json) links
the artifact and closeout gates. The
[source evidence](../evidence/release_0.29.2_source.json),
[installed evidence](../evidence/release_0.29.2_installed.json) and
[resolved closures](../evidence/release_0.29.2_installed_closures.json)
retain the exact qualification scope.
