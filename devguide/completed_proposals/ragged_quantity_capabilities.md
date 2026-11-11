---
summary: Qualify object-row quantities and diagnose unsupported backend operations.
issue: uibcdf/pyunitwizard#148
status: resolved
opened: 2026-11-11
closed: 2026-11-11
verification: reproduced
area: [construction, conversion, interoperability]
guard: tests/test_ragged_quantities.py::test_astropy_rejects_object_rows_with_actionable_diagnostic
normative:
blocked_by: []
supersedes: []
---

# Object-row quantity capabilities

MolSysMT's neighbor compatibility output stores numeric row arrays in a
NumPy object array. Flat numeric distances with CSR offsets provide an
alternative representation. [Consumer #693](https://github.com/uibcdf/molsysmt/issues/693)

The provider reproduction on Python 3.14, NumPy 2.4.6, Pint 0.25.3,
OpenMM 8.6.1, unyt 3.1.0 and Astropy 8.0.1 shows that Pint, OpenMM
and OpenFF preserve row buffers during direct construction and support
unit scaling. Unyt constructs and extracts the rows in this environment,
and translates them to Pint, but native unit conversion rejects the
nonempty outer containers. Astropy rejects row construction and translation,
including an empty outer object array. Dense object arrays of scalar
numbers retain their native constructor behavior.

Retain successful operations and qualify unequal, equal-length and empty
rows, empty outer shapes, input lifetime, explicit unit scaling and policy
preservation. Give unsupported row operations a public TypeError subtype
with a stable catalog code and actionable flat/CSR or per-row guidance.
Preserve native unit-dimension errors and the existing QuantityRecord
numeric schema.

## Resolution

Retain the successful native operations and document the qualified capability
table and row-buffer sharing contract. Public UnsupportedRepresentationError
is a TypeError subtype with code PUW-ERR-REP-001, backend and operation context
and flat/CSR or per-row guidance. It replaces only native failures identified
as object-row representation failures. Astropy parsing and unyt dimensional
errors preserve their existing routes. No new conversion arithmetic or inert
record schema is introduced.

The test-first reproduction had 19 failing diagnostic cases and 37 passing
capability cases. The final 65-case module adds compatible translations and
isolates its policy; catalog reconstruction and lazy-import controls also pass.
The complete local suite passes 1,149 cases, with three executed skips and five
optional collection skips. Documentation builds. Every future staged-installed
profile requires the core object-row guards; the OpenFF profile also requires
its optional row guard. Synthetic JUnit controls reject missing/skipped guards.

The selected Astropy guard verifies all four row shapes raise the public
TypeError subtype with the stable code, backend/operation and CSR guidance,
protecting the originally generic or incidental constructor diagnostic.
`test_unyt_row_conversion_has_actionable_diagnostic` covers the independent
native conversion restriction. Source policy remains intact and QuantityRecord
continues rejecting object arrays. Release qualification is owned by #150;
consumer receiving remains with MolSysMT #693 and MolSysSuite #186.

## Public delivery — 2026-11-11

Delivered in public 0.29.4 from original source
`d9dd0261d7e1f43624f4dd9356830ab9b126bd14`, after all 29 source jobs
and 30 installed cells passed. The actual public installation passes 126
selected tests with both unsupported-backend guards and buffer-lifetime
checks executed. See [the release record](release_0.29.4.md) for exact
file/digest, optional-profile scope and consumer receiving ownership.
