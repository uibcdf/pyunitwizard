# PyUnitWizard 0.29.3

Published on 2026-11-11 UTC through GitHub and the public `uibcdf` Conda
channel. The tag identifies source `c81916e65ce61e905008e8931af3c0e527157251`.
[GitHub Release](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.3)

The virtual `pyunitwizard.main` compatibility module identifies the package
initializer that creates it through `__file__`, its module spec and its
package parent. Installed-origin validation and Python source introspection
can resolve the creator. Legacy imports retain lazy forwarding, function
identity and their one-time deprecation warning.
[#146](https://github.com/uibcdf/pyunitwizard/issues/146) ·
[PR #147](https://github.com/uibcdf/pyunitwizard/pull/147)

The regression verifies the actual registered module in fresh interpreters,
under both cold start and an active application unit policy. It checks the
creator metadata, policy, loaded adapters and warning state.

The maintenance release uses the existing Python 3.11–3.14 Linux/macOS arm64
baseline and the Python 3.12–3.14 OpenFF profile.
[Release qualification](https://github.com/uibcdf/pyunitwizard/issues/149)

All 29 required source jobs and 30 installed cells passed. The installed
reports contain 12,350 passing entries, including both origin regression
scenarios in every cell. The 140 expected skips cover strict JSON NaN and
the older Ackredit prepared API.

The public noarch file is `pyunitwizard-0.29.3-py_0.tar.bz2` (97,985 bytes),
SHA-256 `aea17b691ce7ff89af9b6584aa54211a4703a35b3f6b7e54f34e43ae8c10bbcb`.
Promotion used the qualified staging file. Independent public main-label
and solver-index verification passed.
[Promotion run](https://github.com/uibcdf/pyunitwizard/actions/runs/42970505926)

Clean public Linux/Python 3.14.10 receiving passed 42 tests and `pip check`.
The actual pinned MolSysSuite SDK accepted the installed origins under cold
start and an active policy, and rejected outside-prefix, symlink and
source-checkout controls.
The served installation, compatibility and backend pages identify 0.29.3.

The source snapshot is verified on Zenodo.
[Version DOI](https://doi.org/10.5281/zenodo.24126869)
MolSysSuite coordinates guide synchronization and client receiving.
[MolSysSuite #185](https://github.com/uibcdf/molsyssuite/issues/185)
