---
summary: Qualify and publish 0.29.0 as the next additive interoperability checkpoint.
issue: uibcdf/pyunitwizard#128
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: inspected
area: [release, packaging, documentation]
guard: tests/test_noarch_conda_publication.py::test_installed_prepared_profile_requires_public_provider_and_real_guards
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Release 0.29.0

What — Publish 0.29.0 with the delivered record extensions (#102/#103/#104/#105)
and completed bounded interoperability inventory #85 (#125/#126/#127).
This supersedes the uncreated 0.28.2 plan. Public version remains 0.28.1 until
the actual publication route succeeds.

How — Preserve provisional status and existing qrec bytes. Execute all required
exact-source gates, stage one immutable Conda file, verify that same digest in
all baseline/storage/OpenFF/prepared installed cells, then publish the canonical
0.29.0 tag and GitHub Release (title exactly `0.29.0`). Promote unchanged bytes,
verify public index/installation and served documentation. Retain receipts for
source, producer, installed file and public poststate; source tests do not waive
installed gates. Notify MolSysSuite in a version-specific issue at each actual
release/package event, stating explicitly what remains pending.

Why — Additive tagged/append/storage and dialect APIs merit a minor release and
a qualified public checkpoint before further development. User authorization
includes direct upstream pushes and publication during this session.

## Required scope

- Baseline Linux/macOS Python 3.11–3.14; actual optional storage/dialect
  providers in source and outside-checkout installed tests without scope skips.
- Actual OpenFF 0.4.0/Pint 0.24–0.25 Python 3.12–3.14; prepared attribution
  and public Ackredit fallback remain separate installed profiles.
- Packaged vocabulary JSON/license resources and real consumer fixtures.
- Clean lint/format, reporting/dependency-policy checks, Sphinx docs and actual
  applicable coverage uploads.
- Guide synchronization belongs to MolSysSuite; source provider delivery does
  not claim adoption in client repositories.

Executed publication identities and observations are recorded below.


## Published outcome — 2026-10-23

Stable Release [0.29.0](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.0)
and independently dereferenced annotated tag identify original source
`cfe067bcc4545c60aaca4c6950f6d84075ee6c36`. All 29 mandatory exact-source jobs
and actual CI/Codecov uploads passed. Eight optional source-wheel probes passed
247 cases each without skips. The pre-tag decision is
https://github.com/uibcdf/pyunitwizard/issues/128#issuecomment-6374828043.

Original producer 40014661788, attempt 1, built
`pyunitwizard-0.29.0-py_0.tar.bz2`, 94,325 bytes, SHA-256
`9169cd302dbda415ebc441ef6f5077dcde834d435626fcf80c179a9013657f34`.
Installed run 40018157605/1 passed 30 cells plus the producer verifier. Native
jobs belong to qualifier `821231dbf188656b6872b5f6866b20e9114c87fb`; the owner
receipt separately binds it to the original source/file. #131 selected core
Astropy rather than unrelated recommended cloud extras. No package was rebuilt.
Every required storage/dialect module executed unskipped in eight storage cells,
and every prepared module in eight prepared cells. Intentional strict-JSON/NaN
and unavailable prepared APIs elsewhere remain classified. The installed Conda
lane excludes its nested source-wheel builder, which source suites execute.

Promotion 40025174221 preserved the original digest. The independent pinned
public verifier confirms both main label and solver index. Release-event route
40025139973 verified the staged decision and skipped both build branches.
Tag policy 40025122590 and archive CI/policy 40024974249/40024974932 passed.
Documentation publication 40025140029 used the original release source; the
served UCUM/ASDF/vocabulary, record-extension and quantity-record pages return
200 with 0.29.0 titles. The gh-pages README identifies the same original source.
The direct HTTP probe requires a browser User-Agent (the default Python agent
received 403); cached search content is not used as current evidence.

A fresh public-only Linux/Python 3.14.9 installation imported the original file
and passed 39 record-array/tagged/append/vocabulary guards without skips, plus
version/origin/digest/resource, empty-base64 and same-dimension refusal checks.
Pip reports no broken requirements. Its freely resolved ArgDigest 0.17.0,
DepDigest 0.15.1, SMonitor 0.22.0, NumPy 2.5.4 and Pint 0.26.2 are retained
separately from the pinned required-floor matrix; this smoke does not claim a
new full matrix for those versions. No publication exception was needed.

Complete safe receipts are `devguide/evidence/release_0.29.0_2026-10-23.json`,
with separately retained source, producer, original archive, installed binding,
all 30 Conda/pip closures and JUnit case classifications alongside it.
Earlier failed candidates/qualifications remain recorded under #129/#130/#131.
The selected guard protects the prepared public-provider profile and required
real regression/reader guards; it does not replace executed science or actual
public availability observations.

The version-specific availability/guide handoff is
[MolSysSuite #132](https://github.com/uibcdf/molsyssuite/issues/132). Canonical
`standards/PYUNITWIZARD_GUIDE.md` SHA-256 is
`4d8ffa308b0a004b0b1caa1fa58a871fb715f200f4864b2c1b18416184afc184`.
Suite receiving owners synchronize client copies and pins; source adoption is
not claimed. All provisional and unsupported-scope limits above remain.
