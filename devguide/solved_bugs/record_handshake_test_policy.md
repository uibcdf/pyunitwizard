---
summary: Isolate the record dimension-handshake regression from session output defaults.
issue: uibcdf/pyunitwizard#139
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: low
verification: reproduced
area: [tests, records]
guard: tests/test_quantity_record.py::test_the_reader_refuses_another_dimension
normative:
blocked_by: []
supersedes: []
---

# Record handshake test policy isolation

What — Candidate `85c9bf8e398f03df6cc5490ea5e99ed1ff94cc08` failed full-matrix
Linux/Python 3.12 job 127471328777 in run 42091756904/1. The positive
dimension-handshake assertion inherited unyt from its worker's prior policy,
then tried Pint's canonical `nanomolar` spelling. The failed run retains one
failure, 971 passes and 21 classified skips. No runtime failure is waived.

How — Reproducing the same selector under four explicit session defaults
first gives two failures (unyt and Astropy) and two passes (Pint and OpenMM).
Those adapters already require a supported explicit concentration spelling;
`mole/liter` is documented. Select Pint explicitly for the handshake-only
assertions, retain wrong-dimensionality refusal and strengthen wrong-unit
refusal to `RecordError`. Exercise all four session defaults and assert the
test operation does not overwrite the caller's policy. Separately test the
documented unyt/Astropy reader route with explicit `mole/liter`, independent
physical-scale assertions and unchanged sealed input.

Why — xdist worker order must not choose an unrelated output adapter for a
dimension-handshake regression. This correction tests existing contracts;
it does not add concentration aliases, change backend behavior or weaken the
reader's expected dimensions. Source/internal observations remain separate
from required exact-candidate release and installed-file evidence under #138.

Verification — The focused module passes 68 cases with one intentional
strict-JSON/NaN skip. The full suite on twelve workers passes 1,015 cases,
with three executed-case skips and five optional module-collection skips
(eight JUnit entries total), plus the existing deprecated-main warning.
An initial full run passed 1,014 cases but failed the stale-index guard;
regenerating the new report's index repairs that administrative failure.
Ruff lint/format and all 22 dependency routes pass. No runtime implementation
or public adapter behavior changes. The selected original test is the durable
handshake guard; the added reader test protects the documented non-default
application route and physical scale. Exact test-input and JUnit identities
are retained in `devguide/evidence/record_handshake_policy_2026-11-05.json`.
Release #138 must still qualify the corrected candidate in all required native
source jobs and installed cells; passing results from the rejected original
source are not substituted.
