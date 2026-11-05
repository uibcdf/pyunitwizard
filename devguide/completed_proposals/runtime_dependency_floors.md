---
summary: Ground required runtime floors in numerical and canonical-record contracts.
issue: uibcdf/pyunitwizard#134
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: reproduced
area: [dependencies, packaging]
guard: tests/test_quantity_record.py::test_published_vectors_verify_and_are_reproduced_exactly
normative: devguide/compatibility_matrix.md
blocked_by: []
supersedes: []
---

# Runtime dependency floors

What — Adopt the inclusive runtime-floor rule of MolSysSuite #137 without
guessing from the shared environment or imposing a general next-minor ceiling.

How — Declare NumPy >=1.23.5 and Pint >=0.25 in package metadata, the recipe
and maintained runtime inputs. Preserve exact qualification/build/tool pins.

NumPy's consumed dtype/immutable-buffer/shape operations, broadcasting,
`stack`, `isfinite` and `array_equal(equal_nan=True)` are present in the 1.23
line. Its final 1.23.5 maintenance release supports the oldest Python 3.11
baseline. Qualify actual record, measurement, empty-array, tagged/append and
foreign-registry behavior there; newer Python minors select compatible newer
NumPy distributions. This is a deliberately tested supported floor, not a
claim that every earlier NumPy version is scientifically wrong.

Pint has a concrete scientific lower boundary: published qrec vectors encode
the CODATA-2022 dalton. Pint 0.24.4 writes the older 1.6605390666e-27 kg
definition and fails exact vector reproduction; Pint 0.25 introduces the
CODATA-2022 definitions. A Python 3.14.7 control executes 115 cases on each
version: the pre-floor run has one vector failure; 0.25 passes all 115, with
the existing strict-JSON/NaN skip. The source is unchanged between probes.

Why — Unit meaning and canonical stored bytes are part of the consumed
provider contract, beyond whether an import succeeds. Do not change historical
vectors to accommodate the older writer.

## Optional-runtime review

The package declares no optional scientific runtime extras; `_depdigest.py`
contains lazy availability/install hints, not version requirement fields.
Optionality and current qualification closures remain. Ackredit's portable
fallback floor stays >=0.9.0; >=0.11.0 is separately needed for the stable
prepared-provider promise. No new attribution capability is consumed here.

OpenFF 0.4.0 retains the provider's actual Pint <0.26 restriction and its
Python 3.12–3.14 profile. The PyUnitWizard base floor narrows that profile to
Pint >=0.25,<0.26. UCUM's >=0.25 Pint requirement is now covered by the base
floor. Other optional-provider versions in development/CI remain deliberate
qualification pins, not inferred universal minimums or speculative ceilings.
Provider absence, native ABI and actual scientific qualification remain
independent; no optional engine is made mandatory or silently substituted.

Acceptance — Preserve vectors; execute actual lower numerical/provider
profiles, existing newer-provider cases and dependency-route checks. Review
the metadata/recipe/workflow ranges together. Report the source, bounds and
precisely limited evidence back to MolSysSuite #137. No existing public file,
release tag or historical qualification is rewritten.


## Reviewed outcome — 2026-11-05

Actual Python 3.11.18 / NumPy 1.23.5 / Pint 0.25 with public SMonitor
0.16.0, DepDigest 0.11.0 and ArgDigest 0.14.0 passes 181 selected numerical,
record, foreign-registry, measurement, catalog and calorie cases, with one
intentional strict-JSON/NaN skip. Actual Astropy 6.1.7, unyt 3.1.0 and OpenMM
8.6.1 execute the sixteen energy input/default-form combinations there. Pip
reports no broken requirements. An initial thin minimum run lacked unyt and
failed three measurement cases; the recovery installed actual optional backends
in the owned prefix without changing the shared environment.

Pint 0.25 also passes 115 record/registry cases on Python 3.14.7; the same
selection on 0.24.4 has one exact canonical-vector failure. The selected guard
protects the physical/wire contract grounding this lower bound. NumPy's lower
baseline has separate dtype/shape/record cases rather than an invented version
assertion. The complete latest local runtime suite under #137 passes 1,004
cases; its optional absence and strict-JSON classifications remain separate.

Metadata, recipe, runtime inputs, effective OpenFF candidate range and reviewed
workflow fingerprint are aligned. All 22 dependency routes and 23 selected
workflow/reporting/contract cases pass. No generic runtime upper bound was
added, no existing qualified file rebuilt and no optional engine made mandatory.
`devguide/evidence/runtime_dependency_floors_2026-11-05.json` retains exact
minimum/provider scopes, original failing control and individual JUnit digests.
Future publication still needs its own exact candidate and installed matrix.
