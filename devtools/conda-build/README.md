# Conda publication routes

PyUnitWizard builds one `noarch: python` artifact for Python 3.11–3.14.
The recipe freezes the exact Conda version into the ephemeral build source;
the repository's dynamic `versioningit` configuration remains unchanged.
The build workflow accepts either a reviewed direct release or an immutable
staging candidate, as selected in `release_plan.toml`.

Before a release, update the plan to the proposed three-part version and
record the route, reason, reviewer, and required exact-commit workflows.
The full Linux/macOS matrix, release gates, and suite policy check are
required. Run them at the final candidate SHA. A direct route is appropriate
only when no pre-public installed-artifact or coupled-consumer gate is needed;
the registry must confirm that the version is unoccupied. A staged route is
required for a new interpreter, dependency, packaging contract, or other
change that needs clean installed-package evidence before public visibility.

For the staged route, dispatch
`.github/workflows/build_and_upload_conda_packages.yaml` with the exact
`candidate_sha`, `version`, and `build_number` (normally zero). It uploads
only to `uibcdf/label/staging` and retains the route and producer receipts.
Then dispatch `.github/workflows/test_staged_conda_package.yaml` with the
same coordinates and successful staging run ID. The gate checks artifact
digest, source channel, public dependency provenance, package version, and
record, configuration and attribution contracts outside the source checkout.
Baseline and CF/HDF5 profiles cover clean Linux/macOS environments for Python
3.11–3.14; OpenFF covers 3.12–3.14 with its published provider/Pint constraints.
All profiles install the same Conda archive; optional providers come from the
public channels. The gate retains each resolved dependency closure.
Do not publish a stable GitHub Release until every cell passes.

For a staged release, the release event verifies the plan and does not
rebuild. Dispatch `.github/workflows/promote_conda_package.yaml` only after
the stable GitHub Release exists, using the independently verified digest.
It promotes the exact staged file to the public channel and checks the public
record. For a direct route, the release event builds and uploads once to
`main`, then independently checks the public file's digest.

Before claiming public Python 3.14 support, also check clean installation
from each claimed distribution channel, update the README and user
documentation, and request central `admitted` state under
`uibcdf/molsyssuite#29`. Staging and source tests alone are not publication.

## Maintained dependency contract

`devtools/dependency_routes.toml` inventories every recipe, environment and
workflow using the general MolSysSuite `@2` contract, pinned to
`20628bd5dba6d759669b0d444fe657eb1edad33f`. Public requirements remain in
`pyproject.toml`; test/development/backend selections preserve compatible bounds
with review reasons. Run in the resolved runtime environment:

```bash
python devtools/check_dependency_routes.py --suite-root /path/to/pinned/molsyssuite
```

The checked provider must have that exact commit and unchanged tools. Default
invocation reviews all 22 routes and actual installed public floors/ceilings;
science selections, transitive closure and artifact identity remain separate.
The source workflows run this command before tests/builds. Do not refresh workflow
hashes automatically: review changed installation paths before recording hashes.

Publication bootstrap instead supplies `--candidate-sha FULL_SHA --output PATH`.
It checks declarations at that source and delegates native evidence acquisition
to the same pinned provider. The local plan retains the five original workflows
and requires all 29 source job profiles, with executed default dependency checks.
A backlog-only/skipped matrix cannot qualify. The publisher retains the candidate
receipt before any build/upload; it does not rerun science inside bootstrap.
This route does not authorize rebuilding or replacing the existing 0.28.1 file.

The reporting/guard record is uibcdf/pyunitwizard#114. Generic range/recipe/source
negatives are provider-owned; `tests/test_dependency_routes.py` protects this
member's identity, invocation, native profile and publication ordering.
