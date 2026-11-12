# PyUnitWizard 0.29.5

Preparation and qualification are tracked in
[#152](https://github.com/uibcdf/pyunitwizard/issues/152). No public delivery
is claimed by this preparation record.

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
