---
summary: Automatic parser selection retains a backend without string parsing.
issue: uibcdf/pyunitwizard#95
status: partial
opened: 2026-10-04
closed:
severity: high
verification: reproduced
area: [configuration, parsing, testing]
guard: tests/test_configure.py::test_pint_first_demand_selects_parser_after_openmm_loading
normative:
blocked_by: []
supersedes: []
---

# Automatic parser selection after a non-parser backend

## What

Loading OpenMM first sets both the default form and default parser to
`openmm.unit`, despite its adapter advertising `parser = False`. Requesting
`quantity(3, "nM", form="pint")` then loads Pint but retains the unsupported
parser and raises `LibraryWithoutParserError`. The same invalid automatic
default occurs with unyt, physipy and quantities.

The failure mechanism matches six QuantityRecord failures in full-matrix run
[37203652565](https://github.com/uibcdf/pyunitwizard/actions/runs/37203652565),
on macOS/Python 3.13 at source `4792a8a4d2dc5234b2f5df4da59f003a90419c2d`.
The local reproduction proves the configuration defect, not the historical
worker's exact sequence of preceding tests.

## How

Remove `load_library()`'s fallback to the first non-parser library. Leave the
default parser unset until a parser-capable backend is loaded. Preserve the
first default form and any explicitly selected parser. When parsing is requested
without any available parser, report `LibraryWithoutParserError` for the target
backend rather than a missing-parser-name error. Existing comparison tests
protect that diagnostic compatibility.

## Why

Scientific construction and QuantityRecord serialization must not depend on
whether an unrelated non-parser backend was loaded first. This defect is
independently closable from CI governance/evidence in uibcdf/pyunitwizard#91 and
the QuantityRecord roadmap in uibcdf/pyunitwizard#82.

## What is measured and what is assumed

On Linux/Python 3.14.7 in the complete backend test environment, five new cases
failed before the configuration fix: four invalid automatic defaults and one
first-demand Pint construction after OpenMM. After removing the fallback, four
new parser-diagnostic cases failed until the compatible error was restored.

The first focused configuration/record/parse/conversion run passed 128 tests
with one documented strict-JSON NaN omission. Subsequent parsing/comparison and
fresh-import checks passed 42 tests. The full parallel suite
`python -m pytest --receptor=llm -n 12 tests/` passed 661 tests with 20 skips:
19 require the absent optional Ackredit provider, and one covers the intentional
strict-JSON NaN limitation through a separate rejection test. The existing
`pyunitwizard.main` deprecation warning remains. No hosted macOS reproduction
or exact-candidate CI qualification has been executed for this local change.

## What was refuted

The minimal reproduction fails without serializing a record. The cause is
parser configuration, rather than QuantityRecord JSON/base64 encoding. Resetting
only the affected record tests would conceal the public configuration defect.

## Scope and exclusions

No new parser implementation, backend reordering or explicit-parser override is
introduced. CI routing and the broader record roadmap retain their own issues.

## Acceptance criteria

- Non-parser backends leave the automatic parser unset.
- A later first-demand Pint request succeeds and selects Pint without changing
  the existing default form.
- Explicit parser choices and unsupported-parser diagnostics remain compatible.
- Commit/review the tested change and obtain applicable remote evidence before
  synchronizing closure and archiving this record.

## Dependencies and risks

The fix affects process-global lazy configuration. Regression tests cover the
state transition and observable quantity construction; full-suite verification
includes the parallel execution mode used by the failing matrix. Platform
coverage and optional-provider integration remain outside this local evidence.
