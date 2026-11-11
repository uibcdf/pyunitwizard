---
summary: Qualify and publish the 0.29.3 compatibility maintenance release.
issue: uibcdf/pyunitwizard#149
status: active
opened: 2026-11-11
closed:
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
