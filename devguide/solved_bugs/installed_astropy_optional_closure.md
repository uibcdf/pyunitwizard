---
summary: Qualify the original staged artifact without unrelated Astropy recommended extras.
issue: uibcdf/pyunitwizard#131
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: medium
verification: reproduced
area: [ci, dependencies, release]
guard: tests/test_workflow_contracts.py::test_optional_installed_checks_stop_when_dependency_probe_fails
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Installed Astropy closure selection

What — Exact-file gate 40015415144 at the original source failed pip checks in
several Linux baseline/OpenFF/prepared cells before testing. For example job
120626213009 selected `s3fs-2026.2.0-pyhd8ed1ab_0` with aiobotocore 2.16.1;
the installed Python requirement is aiobotocore >=2.19,<4. The dependency guard
correctly stopped; this is not a scientific test failure or a reason to replace
the staged PyUnitWizard file.

How — Request conda-forge `astropy-base` for installed quantity qualification.
It is the same Astropy Python provider used by `astropy.units`, without the
recommended metapackage's remote-storage/Jupyter extras. Source development
retains its existing recommended frontend tools; the core distribution is now
explicitly declared as a separately selected installer route. Preserve every
baseline/storage/OpenFF/prepared cell, installed test, pip check and public-floor
check. The corrected workflow binds its own source SHA to the original candidate
and exact file through the existing installed-source receipt; source tests and
the installed checker still come from that original candidate.

Why — Official Astropy 8.0.2 Conda metadata includes `s3fs >=2023.4.0` among
recommended extras. Official s3fs 2026.2.0 build 0 permits aiobotocore >=2.5.4,<3
in Conda while its Python metadata requires >=2.19,<4; build 1 corrects that
constraint, but the observed resolver selected build 0. Unit operations do not
need this unrelated remote-storage closure. Selecting the core provider keeps
the operation and all required assertions intact; pip check is never waived.

## Immutable identity and recovery

- Original source: `cfe067bcc4545c60aaca4c6950f6d84075ee6c36`.
- Original staging producer: run 40014661788, attempt 1.
- Original file: `pyunitwizard-0.29.0-py_0.tar.bz2`, 94,325 bytes.
- SHA-256: `9169cd302dbda415ebc441ef6f5077dcde834d435626fcf80c179a9013657f34`.
- Its 29 mandatory source profiles and actual CI/coverage uploads are verified;
  the archive's catalogue JSON and license notice also match the source.
- Corrected qualifier and complete installed/closure receipts are recorded
  in the dated outcome below. Keep the original producer/file unchanged and verify the source/file
  binding explicitly before publication. The generic native-gate reader sees
  the qualifier SHA; the owner receipt must separately bind it to this source.

Release #128 and central version notice `uibcdf/molsyssuite#132` own the
separate public outcome. This does not repair all public Astropy recommended extras or
change any user's shared environment.


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

The selected guard ensures a failed installed dependency check stops before scientific tests can produce a misleading green qualification. Native receipts and closures separately demonstrate that the core Astropy selection fixes the actual original-file qualification without waiving pip checks.
