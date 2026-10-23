---
summary: Preserve OpenMM unit meaning when translating angstrom to unyt.
issue: uibcdf/pyunitwizard#120
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: high
verification: reproduced
area: [forms, interoperability]
guard: tests/forms/test_api_openmm_unit.py::test_openmm_to_unyt_preserves_unit_meaning
normative:
blocked_by: []
supersedes: []
---

# OpenMM and unyt symbol collision

## What

At source 6781afd2c6e046c96a8b176b5f3bf8f157eac84b, converting an OpenMM
angstrom quantity to unyt without a target silently creates amperes. Requesting
nanometers fails with UnitConversionError. Unit-only translation and compound
angstrom/picosecond inputs have the same collision. Discovered during #106's
Topology/coordinate translation evaluation, before accepting timing evidence.

## How

`quantity_to_unyt` forwarded `get_symbol()` to the unyt parser. OpenMM uses `A`
for angstrom, whereas unyt uses it for ampere. Reuse the existing semantic
OpenMM-to-Pint and Pint-to-unyt translators; unit translation already delegates
to quantity translation. This preserves the existing explicit molecular mass
policy rather than adding a parallel alias table or a record-based dispatcher.

## Why

An ordinary molecular coordinate changes physical dimensions. A valid explicit
length conversion then fails. Existing data cannot be repaired by guessing what
a persisted current value originally meant.

## Evidence and scope

Python 3.14.7, OpenMM 8.6.1, unyt 3.1.0, Pint 0.25.3. The new tests initially
produce three failures (length, velocity, unit) and one passing true-ampere
control. Required numeric factors are 0.1 for angstrom→nanometer and 100 for
angstrom/picosecond→meter/second, with array shape and dimensions preserved.
No API, parser, record format or dependency declaration changes. This does not
establish a need for the independent hub proposal.

## Acceptance criteria

- Quantity, unit and compound-length regression tests pass; true current stays current.
- Existing backend conversions and full local suite pass with relevant Ruff/docs checks.
- Central impact notice retains exact source and executed evidence; no new artifact claim.

## Dependencies and risks

Pre-rollout notice: uibcdf/molsyssuite#127. Candidate runtime consumers from the
suite dependency inventory are the eight scientific guide clients; ArgDigest
also has an optional runtime edge. Actual use of this backend pair is unknown.
Client source adoption and public artifact qualification remain separate.

## Resolution and local evidence

The semantic translation replaces display-symbol parsing. Regression-first
execution produced three failures and one passing ampere control. The corrected
adapter passes all 44 focused OpenMM/unyt and backend-matrix tests. The guard
checks actual quantity dimensions and numeric factors, including a compound
velocity; a companion unit-only regression protects the same alias collision.
The adapter test module now imports its adapter explicitly, so the three older
tests no longer depend on another test having populated `puw.forms` first.

The complete local suite, including the new #106 measurement-tool tests, passes
857 tests with one expected strict-JSON/NaN skip and one existing deprecation
warning on Python 3.14.7. The first run was not green: six failures came from
missing physipy/quantities, one from network-denied isolated build dependencies,
and one from not-yet-regenerated report indexes. After index generation, rerun
with network access and task-local physipy 0.2.8/quantities 0.16.4 passes. Those
optional packages reside only under the task root and do not modify the shared
environment. Its pre-existing global dependency conflicts remain independently
owned by uibcdf/molsyssuite#82. Ruff lint and format pass for changed Python files.
Final exact-head hosted evidence belongs in the issue closeout; no public
0.28.1 artifact is relabelled as containing this correction.
