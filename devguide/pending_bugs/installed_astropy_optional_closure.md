---
summary: Qualify the original staged artifact without unrelated Astropy recommended extras.
issue: uibcdf/pyunitwizard#131
status: active
opened: 2026-10-23
closed:
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
- Corrected qualifier SHA, new complete installed run and closure receipts:
  pending. Keep the original producer/file unchanged and verify the source/file
  binding explicitly before publication. The generic native-gate reader sees
  the qualifier SHA; the owner receipt must separately bind it to this source.

Release #128 and central version notice `uibcdf/molsyssuite#132` retain the
pending outcome. This does not repair all public Astropy recommended extras or
change any user's shared environment.
