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

## Publication identity

Tag 0.28.1 targets `25a4bc2468da4ef3af2a638c0bf068becf2acfb4`.
The public noarch archive is `pyunitwizard-0.28.1-py_0.tar.bz2`, SHA-256
`d4654faf93ed4181bf331f7d382379e78f02784f71f678ad19d0ac43d8062cc6`.
Producer 37307676226, installed qualification 37308199459 and promotion
37309227696 preserve those bytes. All 30 installed cells pass, including eight
prepared-attribution cells on public Ackredit 0.10.1. Independent verification
confirms the public main label and solver index; a fresh public-only installation
executes record/storage success/refusal checks and 43 attribution guards.

See the [pre-tag decision](https://github.com/uibcdf/pyunitwizard/issues/112#issuecomment-5994351044)
and archived `devguide/completed_proposals/release_0.28.1.md` for the executed
scope and limits. Complete receipts and installed dependency closures are
retained under `devguide/evidence/`.
