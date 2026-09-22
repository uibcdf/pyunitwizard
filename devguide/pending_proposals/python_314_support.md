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
- The scheduled matrix failure tracked by `uibcdf/pyunitwizard#77` concerns a
  different `parse` assertion on Python 3.13 and is not resolved by this report.

The public Conda recipe is currently Python-specific. Whether the next package
should become `noarch: python` requires an explicit recipe and installed-package
audit; it is not inferred from source-only test success.

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
