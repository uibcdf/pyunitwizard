---
summary: Adopt Python 3.14 support with clean installed-package and release evidence.
issue: uibcdf/pyunitwizard#78
status: active
opened: 2026-09-22
closed:
verification: measured
area: [compatibility, ci, packaging]
guard:
normative:
blocked_by: []
supersedes: []
---

# Python 3.14 support

Current checkpoint, 2026-09-22: GitHub Release 0.26.0 and its exact Conda
`noarch` file are public. Clean Python 3.14 installations from the public
Conda channel and the released source tag passed. Central `admitted` status
and the canonical Python 3.14 README badge are the remaining governance
steps; this report stays active until they are complete.

## What

Extend PyUnitWizard's supported interpreter range from Python 3.11–3.13 to
3.11–3.14, following the phased transition in `uibcdf/molsyssuite#29`.
Do not claim public support until an exact public release and independently
verified clean installations agree with the metadata and CI evidence.

## How

1. Keep the existing Python 3.13 development baseline while expanding the
   declared range, representative CI, release gates, Conda environment bounds,
   recipe, and user-facing support statements.
2. Run the full source suite on Python 3.14 with the optional backends used by
   the release suite, and retain the older interpreter lanes.
3. Build an exact candidate, test installed artifacts in clean environments,
   and stage before publication because this changes the interpreter contract.
4. Verify the public Conda package and any other claimed distribution channel
   independently after release; then request `admitted` in the central registry.

The test-order defect in `tests/forms/test_api_astropy_unit.py` was discovered
during feasibility work. That test now imports its adapter explicitly; it does
not require a public API change.

## Why

SMonitor 0.16.0, DepDigest 0.11.0, and ArgDigest 0.13.0 are already publicly
available with Python 3.14 support. PyUnitWizard is the next core library in
the dependency chain. Its current metadata and workflow matrices still stop
at 3.13, so source success alone cannot be advertised as support.

## What is measured and what is assumed

- On 2026-09-22, a temporary Linux CPython 3.14.7 environment resolved public
  `uibcdf` SMonitor 0.16.0, DepDigest 0.11.0, ArgDigest 0.13.0, and Pytest
  Receptor 1.1.0, with NumPy and Pint. Optional OpenMM, Unyt, Astropy, Pandas,
  Matplotlib, SciPy, Quantities, and PhysiPy were added from published wheels.
- From the checkout, `python -m pytest --receptor=llm -n 12 -p no:cacheprovider
  -q tests` passed all 528 tests after the Astropy test import was made
  independent of collection order. This is source compatibility evidence on
  Linux, not installed-wheel, Conda, macOS, or hosted CI evidence.
- A standalone Astropy test module failed with the original implicit import
  on both Python 3.13 and 3.14. It was a pre-existing test defect, not a
  Python 3.14 regression.
- The complete source suite also passed 528 tests under local Python 3.13
  after the test fix, using 12 workers and the LLM receptor.
- The target interpreter bound, Python classifiers, Linux/macOS full-matrix
  lanes, release-test lane, and development environment bounds were aligned
  at commit `905aebf`. Hosted run `35706809548` passed all eight full-suite
  Linux/macOS × Python 3.11–3.14 cells at that exact SHA. GH Run Receptor and
  an independent GitHub job query agree; a ninth scheduled-monitor job was
  skipped because the run was manually dispatched. The public README and
  documentation still state the delivered 3.11–3.13 range until admission.
- The initial hosted shared-policy run `35706813034` failed on `PYTHON_RANGE`
  because immutable `policy-v1.4.3` predates the central authorization. This
  is a policy snapshot mismatch, not a runtime or metadata failure. The
  replacement `policy-v1.4.4` was published from `uibcdf/molsyssuite@ebdcf49`
  and the local caller now pins it. Hosted policy run `35708012251` passed at
  component commit `2dbd9bc`; an independent GitHub query confirmed its SHA
  and successful conclusion.
- Release-gate run `35708015351` passed at the same commit: four Python
  3.11–3.14 tests-and-contracts jobs, one Python 3.13 wheel packaging smoke,
  and one documentation build. GH Run Receptor and GitHub agree. This is not
  a staged or public Conda package check.
- The scheduled-matrix monitor `uibcdf/pyunitwizard#77` exposed an
  independently tracked `parse` error-contract defect. Its deterministic
  reproduction and fix are recorded under `uibcdf/pyunitwizard#79`.

- The Conda recipe and release workflows are being converted to a single
  `noarch: python` build with a committed direct/staged release decision.
  The first 0.26.0 candidate is staged; it cannot be promoted merely because
  source tests passed. Exact-commit CI, producer receipts, clean installations,
  digest comparison, and public-channel verification remain separate gates.
  The recipe noarch choice follows a source inventory with no compiled
  PyUnitWizard extension; native optional backends remain dependencies.
- The Python and Conda runtime requirements now share the admitted public
  SMonitor 0.16.0 and DepDigest 0.11.0 floors. The changed recipe and release
  route passed 36 focused local tests before the staged verifier was pinned
  to the candidate SHA; after that pin and a formatter correction, both
  Python 3.13 and 3.14 full local suites passed 566 tests with 12 workers and
  `--receptor=llm`. Conda render produced one `noarch` coordinate.
  Before the 0.26.0 tag exists, it
  naturally derives the existing 0.25.0 tag, so that render is a shape check,
  not evidence of a 0.26.0 artifact.
- The first exact-commit shared-policy run at `55253ba` failed the Python
  formatting step, despite passing functional tests. The affected new files
  were formatted and the repository-wide Ruff formatting check now passes.
  The failed run is retained as diagnostic evidence, not counted as a gate.
- At `3ee5d01`, hosted full matrix run `35712086674` passed all eight
  Linux/macOS × Python 3.11–3.14 test cells (the scheduled monitor was
  skipped on manual dispatch). Release gates `35712086712` and suite
  policy `35712087441` passed at the same SHA. GH Run Receptor and
  independent GitHub SHA/conclusion checks agree.
- Staging producer run `35712625482` passed at `3ee5d01` and retained
  both the route receipt and the `events@1` producer receipt. Installed
  artifact run `35712957758` passed its receipt gate and all eight clean
  Linux/macOS × Python 3.11–3.14 installations. This proves staging only;
  at that point there was no 0.26.0 public package, tag, or GitHub Release.
- A final documentation audit found public pages still limited to 3.13 and
  an unsupported `pip install pyunitwizard` instruction. The public PyPI
  index returned no matching PyUnitWizard distribution on 2026-09-22.
  README, Installation, Quick Start, compatibility matrix, and release
  instructions were corrected for the 0.26.0 tag. The documentation HTML
  build succeeded locally without warnings. Since this changes
  the candidate SHA, the old staged `py_0` file is evidence for the prior
  commit only. This required repeating the exact-commit gates and staging
  `py_1` before release.
- Documentation-candidate policy run `35714016742` rejected a Python 3.14
  README badge with `PYTHON_BADGE`: the central badge generator correctly treats
  only `admitted` support as public. Keep the canonical 3.11–3.13 badge
  through the pre-public tag while the version-scoped prose documents what
  0.26.0 will support. After independent public verification and central
  admission, update the badge on `main`; do not relax the common policy.
- Final-candidate matrix run `35714401355` found an Ubuntu/Python 3.12
  failure in `test_parse_rejects_non_string_input`. The input-type check
  occurred after parser resolution and was test-order-sensitive. Issue
  `uibcdf/pyunitwizard#79` owns the fix; publication was held until a new
  exact-commit matrix passed.
- Final release commit `026be28d9530077d57f92cbd5fd1755c0982c596`
  passed 566 local tests on each of Python 3.13 and 3.14, the eight
  Linux/macOS × Python 3.11–3.14 hosted matrix cells in run `35715344397`,
  release gates `35715344393`, and suite policy `35715345024`. All three
  hosted runs have the same exact SHA. The parsing defect is fixed and
  separately guarded under `uibcdf/pyunitwizard#79`.
- Staging run `35715749149` built only
  `pyunitwizard-0.26.0-py_1.tar.bz2` from that SHA. Run `35716044649`
  passed producer provenance and all eight clean Linux/macOS × Python
  3.11–3.14 installations. The producer receipt and independent staging
  registry record agree on SHA-256
  `3689855787a82b7dc942c6b3a71f40733f4f2633c3509f10c12b45892e9ae1a9`.
  The earlier `py_0` artifact is not the release artifact.
- Numeric tag and stable GitHub Release `0.26.0` point to the release SHA.
  The release-triggered Conda run `35716501517` verified the staged route
  without rebuilding. Promotion run `35716642205` moved the digest-matched
  `py_1` file to `uibcdf/noarch`; a fresh public-channel query independently
  returned the same filename, noarch status and SHA-256.
- A clean Linux/Python 3.14.7 Conda environment installed public
  `pyunitwizard=0.26.0=py_1`, SMonitor 0.16.0 build `py_1`, and DepDigest
  0.11.0 build `py_2` solely from public `uibcdf` and conda-forge.
  The Conda record points to `uibcdf/noarch` with the verified digest,
  metadata and imported version equal 0.26.0, import resolves inside the
  environment, and a nanometer quantity smoke test passed.
- Public PyPI index queries found no PyUnitWizard, SMonitor, or DepDigest
  distributions. A second clean Linux/Python 3.14.7 environment installed
  the latter two from public Conda, then installed the Git tag with
  `pip --no-deps`. Pip resolved the exact release commit, built a
  `py3-none-any` wheel, and installed PyUnitWizard 0.26.0. Its
  `direct_url.json`, imported version and API smoke test passed. Public
  guidance now requires Conda dependencies before this source route; it
  does not claim standalone PyPI installation.

## What was refuted

- The initial minimal-environment failures were missing optional backends,
  not evidence that PyUnitWizard was incompatible with Python 3.14.
- The Astropy adapter test failure was not specific to Python 3.14.

## Scope and exclusions

This proposal covers Python interpreter support. It does not extend the
platform support statement to Windows, resolve the separate scheduled-matrix
incident, or change the runtime units API.

## Acceptance criteria

- Package metadata, active CI, release gates, Conda recipe and environments,
  documentation, and the central transition state agree on the target range.
- Full required source CI passes for Python 3.11–3.14 on supported platforms.
- An exact candidate has clean installed-package and optional-backend evidence
  for the target range before public release.
- Every claimed public channel is independently verified at Python 3.14 from
  a clean environment, including installed version and provenance.
- The issue closes with a mechanically addressable test guard or normative
  document and the report moves to the completed-proposals archive.

## Dependencies and risks

The optional-backend stack can make Conda solving expensive and may differ
between channels. Keep code feasibility, Conda resolution, staging, and public
delivery as separate gates, and do not silently downgrade any one of them.
