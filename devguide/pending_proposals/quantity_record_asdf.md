---
summary: Bind native Astropy quantities to complete sealed ASDF snapshots.
issue: uibcdf/pyunitwizard#126
status: active
opened: 2026-10-23
closed:
verification: measured
area: [storage, interoperability]
guard:
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
Qualification remains pending; local tests alone do not qualify 0.29.0.
