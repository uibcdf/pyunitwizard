---
summary: Preserve MIT code and CC-BY vocabulary notices in modern distribution metadata.
issue: uibcdf/pyunitwizard#135
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: reproduced
area: [packaging, dependencies, licensing]
guard: tests/test_distribution_licenses.py::test_sdist_and_rebuilt_wheel_preserve_declared_notices
normative:
blocked_by: []
supersedes: []
---

# License metadata and backend review

What — Review actual license scope and build requirements under MolSysSuite
#162. Preserve the original MIT copyright and the packaged QUDT/UO catalogue's
separate CC-BY-4.0 provenance; the distribution is not exclusively MIT.

How — Use aggregate SPDX `MIT AND CC-BY-4.0` with explicit original `LICENSE`
and `pyunitwizard/vocabularies/NOTICE.md` paths. The implementation remains MIT;
the bounded derived catalogue retains its existing CC-BY license. This records
existing obligations and changes neither text nor copyright. Remove the
redundant deprecated MIT classifier. Require Setuptools >=77.0.3 for PEP 639,
preserving versioningit >=3.0 and Python 3.11–3.14. Align build/host and test
routes, including direct no-build-isolation consumers. Remove the stale
manifest reference to the nonexistent former versioneer.py implementation.

Why — A working modern backend can hide an unsupported declared backend
minimum, and a source LICENSE does not by itself prove notice preservation in
the wheel. The actual catalogue notice explicitly distinguishes data licensing
from the MIT implementation; replacing its license with a generic MIT entry
would be inaccurate.

Acceptance — An actual package build inspects wheel and sdist metadata and
original notice/resource bytes, then builds and checks a wheel from the sdist.
The guard fails on the original source (missing SPDX expression and admission
of pre-feature Setuptools). Execute it using current tools and deliberately
selected Setuptools 77.0.3/versioningit 3.0.0. Retain exact artifact inventories,
hashes and versions. These are local distribution/notice checks; actual Conda
publication, installed/scientific/platform qualification and a future release
remain separately due. Do not rebuild or replace old published files.


## Review completed — 2026-11-05

The real distribution guard passes using Python 3.14.7 / Setuptools 84.0.0 /
versioningit 3.3.0 and deliberately selected Python 3.11.18 / Setuptools
77.0.3 / versioningit 3.0.0. Both tests fail on the original source and pass
on the correction. Actual source-wheel, sdist and rebuilt-wheel metadata
contains the aggregate SPDX expression and both explicit License-File entries;
original MIT/attribution bytes and packaged catalogue/notice bytes match.
The test retains all three archives in its owned fixture and safely extracts
only the locally built sdist. No runtime dependency, old notice or copyright
is rewritten by this metadata migration.

Metadata, Conda host/build/bootstrap and scientific-test build tools are
aligned. The latter are needed because the real distribution test invokes
public PEP 517 backend hooks without isolation, rather than assuming a
transient installer backend is available. All 22 dependency routes pass.
The obsolete missing versioneer.py manifest entry is removed; versioningit
continues to own package versions. Ruff and warning-free Sphinx checks apply.

Exact input hashes, six archive hashes, backend generators and original
notice/resource identities are retained in
`devguide/evidence/license_metadata_2026-11-05.json`. The archive guard proves
these licensing payloads, not installed scientific behavior, a full backend
version matrix or a public Conda file. Future release/installed/public gates
remain due for the future candidate. Existing 0.29.0 bytes stay unchanged.
