# PyUnitWizard 0.29.5

Published on 2026-11-12 UTC through GitHub and public `uibcdf` Conda, from
original source `1783fab011a99567f26e988479ee7dd74c494c6f`.
[GitHub Release](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.5) ·
[Qualification #152](https://github.com/uibcdf/pyunitwizard/issues/152)

Concurrent first quantity/unit requests wait for the selected backend and
parser configuration to finish. This corrects valid first-use calls failing
with LibraryWithoutParserError or observing incomplete dispatch state.
The existing reentrant registry lock allows same-thread recursive
configuration; idle warm admission and lazy optional loading remain.
Native initialization errors propagate, and a waiting reader may initialize
after a failed first attempt. Caller unit policy and public signatures remain.
[#151](https://github.com/uibcdf/pyunitwizard/issues/151)

Fifteen fresh-process guards cover factory, explicit/configured/context Pint,
configured OpenMM/unyt/Astropy, coordinated pre/post-registration readers,
recursion and failure recovery. Ordinary public unit preparation before
starting workers is documented; no new preparation API is needed.
Process-global policy remains shared, and free-threaded Python is not qualified.

The installed-consumer test fixture snapshots finite tracked/current
nonignored source inputs instead of recursively copying tooling and its own
nested temporary output. This test-only correction is
[#153](https://github.com/uibcdf/pyunitwizard/issues/153).

All 29 exact-source jobs and 30 installed cells pass on Linux/macOS arm64,
Python 3.11–3.14 (OpenFF 3.12–3.14). Installed reports contain 14,726 passing
entries and 164 expected optional-profile skips. Every cell executes all
fifteen fresh-process cold-admission cases and prior mandatory guards.

Public file `pyunitwizard-0.29.5-py_0.tar.bz2` is 98,829 bytes, SHA-256
`4f348207721f7f57400d697506c9149e9a6733e4ff010ce82b915731b00ecac7`. Promotion preserves the staged
archive; independent main-label/index verification passes. Clean public-only
Linux/Python 3.14 receiving passes 141 selected tests, pip check and actual SDK
positive/negative origin controls. Optional OpenFF is explicitly deselected
there and qualified in its six installed cells.

The installation, compatibility and backend pages serve 0.29.5 and the
reviewed contract. [MolSysSuite #194](https://github.com/uibcdf/molsyssuite/issues/194)
owns canonical-guide synchronization and consumer receiving coordination.
Zenodo verifies the source snapshot under [version DOI](https://doi.org/10.5281/zenodo.24154809).
[Complete publication record](completed_proposals/release_0.29.5.md)
