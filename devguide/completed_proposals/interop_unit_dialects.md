---
summary: Coordinate optional interoperability forms and physical-unit dialects.
issue: uibcdf/pyunitwizard#85
status: resolved
opened: 2026-09-24
closed: 2026-10-23
verification: inspected
area: [forms, units, interoperability]
guard: tests/test_workflow_contracts.py::test_staged_artifact_profile_executes_new_storage_and_codec_guards
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

## Maintainer-selected completion — 2026-10-23

The maintainer selected completion of the bounded inventory and publication of
0.29.0 instead of the uncreated 0.28.2. Independently owned slices are now:

- UCUM #125: actual case-sensitive ucumvert 0.3.2, the observed 343-row
  Sabueso/ChEMBL concentration/percentage boundary, and explicitly qualified
  physical atoms. Unchecked beta-provider aliases are refused; a reproducing
  guard catches its angular-minute/time-minute mismatch.
- ASDF #126: actual asdf 6.0.0/asdf-astropy 0.11.0 native quantities bound to
  sealed homogeneous multiplicative snapshots, using six real Gaia proper-motion
  pairs from the official Astropy tutorial and retained source provenance.
- QUDT/UO #127: explicit kinds and unit IRIs for hertz, becquerel and radians per
  second; pinned original authoritative vocabularies, reviewed local alignments
  and Gaia's kind-sensitive angular-rate workflow. UO unit IRIs are not kinds.

The implementation and its source/original-file qualification are complete,
as recorded in the dated outcome below. This closes the bounded inventory.
The maintained contract is `docs/content/user/unit-dialects.md`.

Completion is bounded to the identified consumers. Further CF calendar/time-origin
coordinates, complete clinical/astronomy schemas and other ontology entries are
outside this inventory's acceptance contract; a future measured consumer needs
its own issue and acceptance criteria. Molecular time intervals do not justify
calendar semantics. This boundary is recorded in the 2026-10-23 API admission
addendum rather than claiming unimplemented standards conformance.

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
`devguide/completed_proposals/quantity_record_hdf5.md`. The 2026-10-23 completion slices above retain their own qualification evidence.


## Qualified outcome — 2026-10-23

Source `cfe067bcc4545c60aaca4c6950f6d84075ee6c36` passed all 29 mandatory
source jobs and routine CI, including actual Codecov coverage/test-result uploads.
The eight source storage/dialect wheel probes executed 247 cases each without
skips on Linux/macOS arm64, Python 3.11–3.14. Actual providers are ucumvert
0.3.2, asdf 6.0.0 and asdf-astropy 0.11.0; Pint 0.25.3 and 0.26.2 are covered.

Original producer 40014661788, attempt 1, built only
`pyunitwizard-0.29.0-py_0.tar.bz2` (94,325 bytes), SHA-256
`9169cd302dbda415ebc441ef6f5077dcde834d435626fcf80c179a9013657f34`.
All 30 exact-file installed cells and the producer verifier passed run
40018157605, attempt 1, at qualifier
`821231dbf188656b6872b5f6866b20e9114c87fb`. Its owner binding explicitly
retains the original source/file identity; #131 corrected only the qualifier's
Astropy dependency selection. The archive was not rebuilt.

Every required storage/dialect/record-extension module executed without skips
in all eight storage cells; every prepared-attribution module executed without
skips in all eight prepared cells. Whole-run counts retain the intentional
strict-JSON/NaN skip and unavailable prepared-API skips in fallback profiles.
The copied installed lane excludes its nested source-wheel builder because it
qualifies the original Conda file; source suites separately execute that builder.

Native receipts and actual source-wheel facts are retained in
`devguide/evidence/release_0.29.0_source.json` and
`devguide/evidence/unit_dialects_source_installed_2026-10-23.json`.
Archive bytes/resources, original-source binding, all 30 dependency closures and
individual case classifications are retained in `devguide/evidence/` as
`release_0.29.0_staged_bytes.json`, `release_0.29.0_installed.json` and
`release_0.29.0_installed_closures.json`. These qualify the implemented boundary;
publication/public-index observations remain separately owned by #128. All
provisional limits and consumer-owned scientific meanings above remain.

The selected guard retains the complete installed storage/dialect inventory and explicit skip rejection. Runtime meaning and actual provider qualification belong to the child guards and retained native evidence; this completes only the measured bounded inventory, not every possible standard.
