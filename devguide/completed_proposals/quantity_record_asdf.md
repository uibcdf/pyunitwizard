---
summary: Bind native Astropy quantities to complete sealed ASDF snapshots.
issue: uibcdf/pyunitwizard#126
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: measured
area: [storage, interoperability]
guard: tests/storage/test_asdf.py::test_resealed_native_frequency_cannot_be_relabelled_as_activity
normative: docs/content/user/unit-dialects.md
blocked_by: []
supersedes: []
---

# Native ASDF quantity snapshots

What — Add optional `qrec-asdf/0.1` under #85, reusing qrec metadata, typed
restoration and receiver handshakes instead of defining a second quantity model.

How — Native `astropy.units.Quantity` carries a detached typed array and unit;
a binding header seals the native spelling together with the original qrec
metadata. Reads check native physical dimensions/scale, dtype/shape, original
value seals and explicit expectations. Native provider checksums are enabled.
File publication uses an owned same-directory temporary and exclusive hard link;
failure never replaces an existing path. Tree helpers are independently usable.

Why — Native ASDF quantities remain readable with actual astronomy tools, while
the additional binding protects the unit together with the values.

The measured input is six actual Gaia DR2 proper-motion pairs around HD 219829
from `astropy-learn/tutorial--astropy-coordinates`, immutable source
`9fa08d3cd87fcaa90ab1667dacd795f88ef36b91`, file
`HD_219829_query_results.ecsv`, SHA-256
`b53a45c75044f4852b4d90d37aff923e4105545176317a526e6522092142bdf7`.
`tests/data/gaia_proper_motion.json` retains original values, unit and source IDs;
the source BSD license is retained beside it. The consumer explicitly converts
mas/year to radians/second and assigns angular velocity. This is a new archival
snapshot of real Gaia values, not an archive originally published by Gaia.

## Acceptance and exclusions

Qualify actual asdf 6.0.0 and asdf-astropy 0.11.0 in source and installed
Linux/macOS Python 3.11–3.14 probes. Cover native independent reads, unchanged
record identity, scalar/empty/array numeric types, corruption/relabel rejection,
unsealed native rejection, missing providers and failure cleanup.

The initial binding is homogeneous and multiplicative only. Affine units require
explicit conversion to Kelvin; tagged arrays, coordinate frames/epochs, native
unsealed migration, remote/partial/streaming/archive-append interfaces and ASDF
schemas for entire astronomical datasets are outside scope. A digest establishes
integrity, not authentication or truth of a consumer's asserted scientific kind.
Source and original-file qualification are recorded below; local tests alone
do not qualify publication of 0.29.0.


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

The selected guard prevents a native Hz-to-Bq relabel from passing merely because Astropy gives both units the same SI dimensions. Actual native round trips, corruption and exclusive publication have separate guards.
