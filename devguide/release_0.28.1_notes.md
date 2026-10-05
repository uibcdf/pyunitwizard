# PyUnitWizard 0.28.1

PyUnitWizard 0.28.1 reduces repeated declaration copying during optional
prepared backend attribution (#111). Warmed Pint/unyt dispatch reuses immutable
declaration plans after validating current metadata values. Backend-version and
nested metadata changes invalidate the plan; independent result captures and
registry-conflict checks remain effective. Scientific results and public API
signatures are unchanged.

Controlled paired installed measurements show improvements in captured scalar
and array paths. These measurements hold the provider and scientific dependencies
fixed; they do not promise a universal percentage or a cold-start improvement.
Raw samples, identities and limits are retained in
`devguide/evidence/backend_declaration_plans_2026-10-05.json`.

Ackredit remains optional with the existing >=0.9.0 floor. The 0.9 fallback is
retained, and prepared attribution is additionally qualified with public
Ackredit 0.10.1. Prepared/observer interfaces and the record, measurement,
OpenFF, CF and HDF5 interfaces introduced in 0.28.0 remain provisional.

The distribution route is the uibcdf Conda channel plus conda-forge. Baseline,
CF/HDF5 and prepared-attribution installed qualification covers Linux and
macOS arm64 on Python 3.11–3.14; OpenFF covers Python 3.12–3.14 with
openff-units 0.4.0 and Pint >=0.24,<0.26. No PyPI publication or stable 1.0
admission is claimed.

The exact source, immutable Conda file, executed gates and public verification
are tracked in [uibcdf/pyunitwizard#112](https://github.com/uibcdf/pyunitwizard/issues/112).
