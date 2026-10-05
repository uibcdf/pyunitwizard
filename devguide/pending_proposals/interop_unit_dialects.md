---
summary: Coordinate optional interoperability forms and physical-unit dialects.
issue: uibcdf/pyunitwizard#85
status: partial
opened: 2026-09-24
closed:
verification: inspected
area: [forms, units, interoperability]
guard:
normative: devguide/api_freeze_pre_1.0_decision.md
blocked_by: []
supersedes: []
---

# Interoperability forms and unit dialects

What — Coordinate the separately qualified OpenFF, CF/UDUNITS, ASDF, UCUM
and QUDT/OBO unit exchange surfaces identified while reviewing #83.

How — Start each independently useful operation from a measured consumer;
keep optional dependencies lazy and signatures explicit. Core forms own object
conversions; dialect tools own spellings/semantics; storage tools own verified
bindings. Consumers retain field association, their scientific schemas and
legacy migration. Do not implement popular formats or guess name tables without
an identified boundary and actual-provider conformance evidence.

Why — A central owner prevents inconsistent downstream translations and labels
that silently change the meaning of stored values. Equal dimensions do not
establish a common quantity kind or equal numeric scale/offset.

## Delivered and bounded slices

- Cross-registry Pint verification (#84) is implemented and reused by OpenFF.
- OpenFF (#86) is qualified for the actual conda-forge 0.4.0 distribution;
  its record is `devguide/completed_proposals/openff_compatibility.md`.
- The CF physical-unit slice (#108) serves the measured H5MSM/HDF5 (#101)
  boundary using actual cf-units/UDUNITS and explicitly negotiated spellings.
  Its scope excludes calendar reference times, arbitrary numeric transforms,
  logarithmic and unknown units, whole-CF-dataset conformance and kind inference.
  Temperature readers/writers must both declare on-scale/difference semantics.

## Remaining independently justified work

UCUM needs a measured clinical/biomedical exchange case and case-sensitive parser
and emitter conformance before implementation. Codes must not be treated as Pint
aliases (for instance, M has different semantics).

ASDF needs an actual astronomy archival quantity/array and installed
asdf-astropy interoperability evidence. Existing HDF5 work does not qualify ASDF.

QUDT/OBO annotations need an authoritative vocabulary mapping and an actual
kind-sensitive workflow, such as frequency versus radioactivity. Dimensional
parity alone cannot choose an identifier or semantic equivalence.

Further CF scope, including calendar/time-origin coordinates, needs a separate
consumer and acceptance contract. Molecular time intervals do not justify that
expansion. #85 remains partial after the delivered slices close.

## Acceptance and limitations

Each implemented slice has its own owning issue, tests, documentation, optional
installed/matrix evidence and versioned provisional contract. Closing a child
neither closes this inventory nor qualifies a new public PyUnitWizard release.
Coverage incident #107 is closed after actual uploads recovered during the
0.28.0/0.28.1 publication route. Each future candidate retains its own required
ingestion evidence. MolSysMT adoption of the provider tools is
separate from their qualification in PyUnitWizard; no consumer source is changed
by the local #101/#108 work.

The delivered CF/HDF5 slice is qualified at final runtime
`d4c6089be2f4b8d4c975f31238209ce7348ee4c0`; its receipt is
`devguide/evidence/cf_hdf5_interop_2026-10-05.json`. Final archived records are
`devguide/completed_proposals/cf_unit_dialect.md` and
`devguide/completed_proposals/quantity_record_hdf5.md`. This inventory remains
partial for the independently justified work above.
