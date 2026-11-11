# PyUnitWizard 0.29.2

Published on 2026-11-11 UTC through GitHub and the public `uibcdf` Conda
channel. The tag identifies source `cf40c9fcdd4cd2d18df78a9d8fcef3b2d9516256`.
[GitHub Release](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.2)

- Pint conversions among nm, Å and pm use one binary64 rounding for the
  verified definitions in PyUnitWizard's registry. Existing `convert()`
  and `get_value()` calls preserve the exact cutoff and its immediate
  neighbors at the tested contact boundaries. This covers binary64 scalars,
  float64 arrays and exactly representable integer scalars. Foreign Pint
  registries, active Pint contexts and other units or dtypes use their
  established conversion paths. [#143](https://github.com/uibcdf/pyunitwizard/issues/143)
- The canonical initialization example checks whether Pint is loaded before
  requesting its registry cache. An existing application policy takes
  precedence. [#144](https://github.com/uibcdf/pyunitwizard/issues/144)
- Expected negative probes skip construction of their event payload when
  the active SMonitor level filters DEBUG. A switch to DEBUG restores the
  existing catalog event. In the local 2,000-probe comparison the median
  went from 211 to 13 ms. [#141](https://github.com/uibcdf/pyunitwizard/issues/141)
- Numeric quantity construction with a string unit avoids an intermediate
  quantity when Pint is the parser and output form. The median for 4,566
  constructions went from 110 to 89 ms. Two synthetic OpenCASTp analyses
  preserved every result field. End-to-end timing varied by input.
  [#142](https://github.com/uibcdf/pyunitwizard/issues/142)

The release retains the existing API, dependency requirements and Python
3.11–3.14 baseline for Linux and macOS arm64. OpenFF uses its existing
Python 3.12–3.14 profile. [Release qualification](https://github.com/uibcdf/pyunitwizard/issues/145)

All 29 required exact-source jobs and all 30 installed cells passed. The
installed JUnit reports contain 12,140 passing entries. Every cell executed
its 27 cutoff boundary cases and the construction and diagnostic regressions.
The 140 expected skips cover strict JSON NaN and the prepared attribution
API on the older Ackredit profile.

The public noarch file is `pyunitwizard-0.29.2-py_0.tar.bz2` (98,016 bytes),
SHA-256 `bb28b9420760b557025163e11c934e096c7b98200cac720100a2db924e9ee617`.
The promotion used the qualified staging file. Independent verification
confirmed the main label and solver index. Clean Linux/Python 3.14.10
receiving passed 35 tests and `pip check`. The served installation,
compatibility and backend pages identify 0.29.2.
[Promotion run](https://github.com/uibcdf/pyunitwizard/actions/runs/42940169699)

Zenodo verified the source snapshot.
[Version DOI](https://doi.org/10.5281/zenodo.24122890)
MolSysSuite coordinates guide synchronization and client receiving.
[MolSysSuite #180](https://github.com/uibcdf/molsyssuite/issues/180)
