# PyUnitWizard 0.29.2

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
