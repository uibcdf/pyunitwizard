---
summary: Qualify and publish the 0.29.3 compatibility maintenance release.
issue: uibcdf/pyunitwizard#149
status: resolved
opened: 2026-11-11
closed: 2026-11-11
verification: measured
area: [release, packaging, provenance]
guard: tests/test_noarch_conda_publication.py::test_staged_profiles_require_runtime_regressions
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Release 0.29.3

## Scope

The release supplies the compatibility-module creator origin correction
from #146 and PR #147. The virtual `pyunitwizard.main` module declares the
initializer that creates it through file, spec and package metadata.
The [release notes](../release_0.29.3_notes.md) describe the delivered behavior.
DockingMT #74 owns receiving the provider revision in its own installed gates.
MolSysSuite #184 tracks the advance consumer-impact notice.

## Qualification

The plan selects staging for one immutable noarch archive and the existing
29 source jobs and 30 installed cells. Each installed cell runs the API layout
suite and requires both cold-start and active-policy creator-origin cases.
The workflow also retains the prior cutoff, construction, diagnostic,
calorie and optional-profile guards. The synthetic JUnit controls check the
pass path and missing or skipped cases for both origin scenarios.

The merged source passed 1,064 local tests, with eight recorded skips
including five optional module collections. Actual PR CI passed 1,026 cases
with 21 conditional skips. Independent review reproduced the actual pinned
SDK failure with the original wheel, accepted the correction and retained
outside-prefix, symlink and source-checkout rejection. That review used
borrowed runtime dependencies. The release will qualify its own installed file.

After source qualification, build the archive once into staging. Verify its
source, resources, metadata and digest, then execute every installed cell
against that file. Promote the qualified digest, independently verify the
public label/index and run clean public receiving with the actual pinned
origin checker. Verify served docs and source archival. Deliver a
release-specific MolSysSuite notice with the package and guide identities.

The newly filed #148 records ragged-array construction behavior for a later
provider capability review. Its report identifies an existing representation
limitation and leaves 0.29.3's compatibility-origin scope intact.

The preparation changes pass 82 focused source, workflow, publication and
reporting tests. The pinned shared checker verifies all 23 dependency
routes with declared and installed public bounds. Ruff and the report
index checks pass.

## Publication outcome

The stable tag and GitHub Release `0.29.3` identify
`c81916e65ce61e905008e8931af3c0e527157251`. All 29 source jobs passed.
Producer 42969436186/1 built the 97,985-byte
`pyunitwizard-0.29.3-py_0.tar.bz2` with SHA-256
`aea17b691ce7ff89af9b6584aa54211a4703a35b3f6b7e54f34e43ae8c10bbcb`.
The archive's 92 tracked Python source files, resources, metadata and
license files match the qualified source.
[Release](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.3) ·
[Producer](https://github.com/uibcdf/pyunitwizard/actions/runs/42969436186)

All 30 installed cells passed in 42969805706/1, with 12,350 passing
entries. Every cell executed both origin cases, along with the prior
required runtime guards. The 140 expected skips concern strict JSON NaN
and the older Ackredit prepared API. Promotion 42970505926/1 retained the
qualified digest. The release event's two build steps were skipped, and
its staged decision step passed.
[Installed matrix](https://github.com/uibcdf/pyunitwizard/actions/runs/42969805706) ·
[Promotion](https://github.com/uibcdf/pyunitwizard/actions/runs/42970505926)

Independent public main-label and solver-index verification passed.
A clean public-only Linux/Python 3.14.10 installation passed 42 tests and
`pip check`. The actual SDK at `95f693be10c9205ab9b912cb53453710a207bf45`
accepted the installed origins under cold start and an active policy.
It rejected outside-prefix, symlink and source-checkout controls.
Its QA dependencies were provisioned in that public receiving environment.
The initial local probe stopped at the temporary filesystem's quota;
receiving completed in a new prefix outside the checkout using the same file.

Canonical guide commit `ef0da74f734ca1ad1503f88891e2fdafc79b2d95` and
its content digest were delivered to MolSysSuite for client synchronization.
DockingMT #74 owns independent consumer receiving.
[MolSysSuite notice](https://github.com/uibcdf/molsyssuite/issues/185)

The updated documentation build and Pages deployment passed. The public
installation, compatibility and backend pages serve 0.29.3 and their
reviewed instructions.
[Pages deployment](https://github.com/uibcdf/pyunitwizard/actions/runs/42971130059)

Zenodo verified the source snapshot at version DOI
`10.5281/zenodo.24126869`.
[Zenodo record](https://doi.org/10.5281/zenodo.24126869)

The [publication receipt](../evidence/release_0.29.3_publication.json),
[source proof](../evidence/release_0.29.3_source.json),
[installed proof](../evidence/release_0.29.3_installed.json) and
[resolved closures](../evidence/release_0.29.3_installed_closures.json)
retain the exact executed scope.
