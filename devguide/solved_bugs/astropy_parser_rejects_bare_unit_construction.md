---
summary: Astropy parser rejects bare unit strings during quantity construction.
issue: uibcdf/pyunitwizard#96
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: high
verification: reproduced
area: [construction, conversion, adapters]
guard: tests/test_conversion_branches.py::test_quantity_with_bare_unit_works_with_astropy_default_parser
normative:
blocked_by: []
supersedes: []
---

# Bare unit construction with the Astropy parser

## What

Full matrix [37219917253](https://github.com/uibcdf/pyunitwizard/actions/runs/37219917253)
on `ef91dcec9a064cbabe767cd6195e32cdac82840d` passes seven cells, including the
previously failing macOS/Python 3.13 cell, but fails four getter tests on
macOS/Python 3.14. Quantity construction passes a bare unit to Astropy's quantity
parser: `angstrom` lacks a number, while `nanometer` is interpreted as `nan`
followed by invalid `ometer`. This is distinct from automatic selection of an
unsupported parser in uibcdf/pyunitwizard#95.

## How

Reuse conversion's existing cached `_parse_unit_string()` for string inputs
requested as `to_type="unit"`. Its numeric-prefix fallback already serves
conversion targets. Construct a neutral quantity from the resolved unit before
the existing conversion/extraction pipeline, preserving numeric quantity-string
and target-unit behavior. Construction calls this same conversion entry point.

The regression also exposes an Astropy-to-Pint spelling mismatch for the
canonical Angstrom unit. Normalize that exact unit to Pint's `angstrom` name in
the existing adapter bridge. This also serves OpenMM/unyt translation through
Pint; it does not add a general unit-dialect mapping.

## Why

The selected parser policy must support ordinary unit construction without
depending on xdist worker order. Reseting only getter tests would conceal a
public construction defect. Reusing the existing operation avoids duplicating
parser-specific fallback logic in construction.

## What is measured and what is assumed

Linux/Python 3.14.7 reproduces the construction failure with Astropy loaded
before Pint. Seventeen new cases cover two bare units across four construction
forms and bare/numeric unit strings across Pint, Astropy and string outputs.
Before the fix, fifteen fail and two pass; after the fix, the focused
construction/getter/parse/record/Pint-conversion run passes 142 tests with the
documented strict-JSON NaN omission.

Both complete local suites pass 678 tests with 20 documented skips, in serial
(29.81 seconds) and with twelve workers (13.09 seconds). Nineteen skips require
the absent optional Ackredit provider; one covers the strict-JSON NaN limitation
through a separate rejection test. The existing main-module deprecation warning
remains; the parallel runner also emitted an unclosed `/dev/null` ResourceWarning
outside its summarized pytest warnings. Ruff/format, syntax compilation,
reporting indexes and the HTML documentation build pass.

Hosted follow-up passes as recorded below. The historical worker's exact
configuration sequence is not reconstructed; the minimal deterministic
reproduction proves the parser boundary problem.

## What was refuted

The scalar-output coercion itself is not reached in the failing getter tests.
Failures occur during quantity construction. Numeric-prefix fallback alone is
insufficient for Angstrom translation to Pint because its emitted spelling
differs between adapters.

## Scope and exclusions

Explicit parser policy and quantity-string parsing remain unchanged. The
broader dialect roadmap in uibcdf/pyunitwizard#85 and CI governance in
uibcdf/pyunitwizard#91 retain their own issues.

## Acceptance criteria

- Bare-unit construction works with Astropy as default or explicit parser.
- Unit extraction retains numeric-string and string-output behavior.
- The canonical Angstrom bridge preserves values and physical units.
- Pass local checks and the hosted full matrix, then archive the guarded record
  and synchronize closure.

## Dependencies and risks

The cached unit parser already owns numeric-prefix fallback. The fix shares it
with construction and unit extraction rather than changing public parser
signatures. Full-suite serial and parallel tests cover configuration interactions.

## Resolution — 2026-10-04

Implementation `71de829a53ab50964f180ac558ea0307510ee0cb` passes
[routine CI](https://github.com/uibcdf/pyunitwizard/actions/runs/37223621178),
[suite policy](https://github.com/uibcdf/pyunitwizard/actions/runs/37223621591)
and [all eight full-matrix cells](https://github.com/uibcdf/pyunitwizard/actions/runs/37223629790),
including macOS/Python 3.14. Each cell executes the suite successfully with 676
passed and 22 documented skips: 19 optional Ackredit-provider cases, two absent
sibling-source integrations and one strict-JSON NaN case with separate rejection
coverage. Exact producer identities, executed steps and limits are preserved in
`devguide/evidence/ci_recovery_2026-10-04.json`.

The durable guard constructs quantities using the Astropy default parser for
angstrom/nanometer across four target forms, checks form/value preservation, and
asserts that parser policy stays unchanged. Its companion unit-extraction cases
cover explicit Astropy, numeric prefixes and string outputs. These assertions
exercise the construction failure before scalar coercion can hide it.
