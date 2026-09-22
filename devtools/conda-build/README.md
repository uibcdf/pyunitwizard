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
an API smoke test in clean Linux/macOS environments for Python 3.11–3.14.
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
