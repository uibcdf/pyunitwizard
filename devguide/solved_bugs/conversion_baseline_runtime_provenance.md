---
summary: Report the actual Python runtime in conversion baseline measurements.
issue: uibcdf/pyunitwizard#121
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: low
verification: reproduced
area: [tooling, performance]
guard: tests/test_conversion_baseline.py::test_baseline_reports_the_actual_python_runtime
normative: benchmarks/README.md
blocked_by: []
supersedes: []
---

# Conversion baseline runtime provenance

## What

`benchmarks/conversion_baseline.py::run_baseline` labels every new result with
the literal Python version `3.13`, regardless of the executing interpreter.
The current routine development environment runs Python 3.14.7. Found while
evaluating #106; this is measurement metadata drift, not a numerical defect.

## How

Replace only the literal with `platform.python_version()`, matching the actual
runtime reporting used by the newer record benchmark. Preserve the string type,
timed cases, telemetry modes and package-version fields. A fresh-process test
runs the real benchmark with one iteration/repeat, checks its emitted runtime
against the executing interpreter and verifies both telemetry case sets remain.
Process isolation keeps the benchmark's policy reset out of the pytest session.

## Why

Incorrect interpreter provenance can invalidate comparisons between performance
snapshots. Installed distribution metadata is not a substitute for runtime or
source identity. Historical measurements keep their original provenance; this
fix does not relabel old JSON files or assert which interpreter produced them.

## Acceptance criteria

- The regression fails before and passes after the metadata correction.
- Relevant Ruff and reporting/index checks pass; inspect applicable final head CI.
- Documentation describes the runtime-version field without changing historical evidence.
- Review remaining issues for concrete pre-0.28.2 work; no release is authorized here.

## Resolution and validation

The benchmark now uses `platform.python_version()`. The fresh-process regression
first fails with `'3.13' != '3.14.7'`, then passes with the actual runtime field.
It executes the real baseline in both telemetry modes rather than mocking the
version or replacing the timed cases. The previous static string type is kept;
new output includes the executing interpreter's patch version. No historical
measurement or scientific package code changed.

Python 3.14.7 local checks: 20 focused tests pass (provenance, report lifecycle and
record benchmark contracts). Repository-wide Ruff lint/format passes, 214 files.
The owned-copy Sphinx build passes without warnings. Report indexes and diff
checks pass. The previous 859-test scientific result remains evidence for its
unchanged runtime scope; this small tool change receives the final head's normal
unskipped CI, with native evidence retained in the issue closeout. No extra
scientific matrix or installed public artifact is claimed.

## Pre-0.28.2 review

The review of actual optional-adapter calls finds two more `.to_pint()` calls
without a shared registry: unyt dimensionality and unyt→OpenMM. This is owned
separately by uibcdf/pyunitwizard#123. Constructor-count reproduction on the
unchanged scientific source gives two constructions for two direct adapter
dimensionality calls, one for two public dimensionality calls (cache hit on the
second), and two for two public OpenMM conversions. Values remain correct.
The issue retains scope, environment and acceptance criteria; this task does not
implement its correction or alter #122's historical Astropy closure.

Recommend #123 as the next bounded patch candidate. #102–#105 and remaining
#85 slices still need their named real consumer/measurement prerequisites;
#44/#52 remain deferred and #87 conditional. No speculative format/dependency
expansion is added and no 0.28.2 tag, artifact or publication is created.
