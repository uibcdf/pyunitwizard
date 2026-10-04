---
summary: Review inherited Python ecosystem policy in PyUnitWizard.
issue: uibcdf/pyunitwizard#89
status: partial
opened: 2026-09-25
closed:
verification: measured
area: [development, integration]
guard: tests/integration/test_ecosystem_smoke.py
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in PyUnitWizard

## What

Review PyUnitWizard's adoption of the MolSysSuite Python developer-tool and support-library
policies under `uibcdf/molsyssuite#6`. Record the two conclusions independently.

## How

Pin pytest-receptor 1.1.0 in the test, development, and release-gate Conda
environments. Select its `ci` profile in every hosted pytest command while retaining
the existing tests, coverage, JUnit report, xdist, and release gates. Use `llm` for
local agent testing. Inspect hosted runs through gh-run-receptor and check the
installed Conda package and command in a native log when needed.

Review SMonitor diagnostics, DepDigest optional-dependency checks, ArgDigest's
optional quantity adapter, and PyUnitWizard's own quantity boundary. Distinguish
tested runtime integration from optional tests skipped by an environment.

## Why

PyUnitWizard is a priority support library in MolSysSuite. Its integration status
cannot be inferred from guide copies or dependency declarations alone. A member-local
issue and evidence are needed before changing the suite inventory.

## What is measured and what is assumed

At filing, all three pytest environments lacked pytest-receptor, and routine CI,
the full matrix, and release gates invoked plain pytest. After the changes,
`PYTHONPATH=. pytest --receptor=llm -q tests` passed locally with 596 passed and
8 skipped. The initial run failed one local-sibling import test because this
temporary checkout's SMonitor sibling was sparse; completing that temporary
clone and repeating the unchanged suite made the test pass. Ruff check and
format, the report-index check, and the MolSysSuite repository checker pass.
No claim is made that all optional integrations are active in the existing
environments.

Routine CI `36102753740` passed at source commit `c8cd856`, with 622 passed and
5 skipped. Its native log confirms the exact `uibcdf` Conda package
`pytest-receptor 1.1.0 py_1` and the `--receptor=ci` command. The policy run
`36102754343`, release gates `36102768017`, and the eight-cell full matrix
`36102767731` passed; the release gates include the full test suite on Python
3.11 through 3.14. All four were first inspected with gh-run-receptor.

For the support-library review, SMonitor is a runtime dependency used for
diagnostic signals and covered by catalog and error-path tests. DepDigest is a
runtime dependency used for optional backend availability, with declaration
and integration tests. PyUnitWizard owns the physical-quantity conversion and
dimensional checks.

Source `00d470773ac136d83a0ec2cde7566999ffda0d0e` pins published ArgDigest
0.13.0 in the development, test, and release-gate environments. Routine CI and
the eight-cell Linux/macOS matrix require an import of the published adapter
before pytest; release gates require it on Python 3.11–3.14. Local integration
smoke passed five tests, and the full local suite passed 634 with three
unrelated skips. GH Run Receptor inspected exact-commit routine CI
`36335377594`, policy `36335377971`, release gates `36335382518`, and matrix
`36335382533`; all passed. Each matrix cell imported ArgDigest 0.13.0 and
passed 634 tests with three unrelated skips. The release-gate API and
integration smoke passed ten tests on every claimed Python minor, with the
published ArgDigest version recorded in each native log. This resolves the
hosted optional-integration evidence gap.

At source `00d4707`, the support-library review remained partial because the public API had
native nontrivial argument checks. Examples included
`configure.load_library()` and `configure.set_standard_units()`; quantity
construction and record reading also validate product-specific physical or
integrity semantics. A test-only ArgDigest dependency does not decide which
ordinary public argument constraints should move to ArgDigest, nor whether a
bounded provider exception is appropriate. ArgDigest declares PyUnitWizard in
an optional extra, so a required reverse edge would also need dependency and
import-order analysis. Resolve that boundary under this issue before claiming
full support-library adoption.

## What was refuted

Installing pytest-receptor alone would not select the compact CI presentation;
the explicit profile is required in each hosted command.

## Scope and exclusions

This review does not change PyUnitWizard's scientific behavior or resolve unrelated
product issues. It does not redesign the shared MolSysSuite policy.

## Acceptance criteria

- All hosted pytest gates invoke `--receptor=ci` with exact published dependency.
- Local tests and Ruff checks pass; hosted routine CI and selected matrix or release
  gates provide evidence for claimed interpreter support.
- The support-library assessment names exercised paths, skips, and any remaining
  limitation in this issue and the MolSysSuite inventory.

## Dependencies and risks

The historical full-matrix monitor `uibcdf/pyunitwizard#77` is closed. Later
parser/configuration failures were resolved under `uibcdf/pyunitwizard#95`
and `uibcdf/pyunitwizard#96`, with eight-cell recovery `37223629790`.

## Runtime boundary and receiving review — 2026-10-04

ArgDigest 0.14.0 is used at runtime for ordinary configuration normalization:
`load_library`, `set_standard_units`, and `add_standard_units` call its
public `pipelines.coercers.to_list` after preserving the existing accepted
container boundary. It provides string wrapping and owned list/tuple
normalization, fixing caller mutation and premature policy reset under
`uibcdf/pyunitwizard#98`. Its import occurs only when configuring or loading
a backend. The simple allowed-container rejection preserves existing exception
types; it does not introduce another digester protocol.

Backend aliases, dimensionality, unit interpretation, conversions, record
schema validation, seals, and compatibility checks are product semantics
owned by PyUnitWizard. Enum/flag dispatch and ordinary Python type errors
need no extra decorator layer. There is no required runtime cycle: published
ArgDigest 0.14 requires SMonitor and DepDigest, while its PyUnitWizard edge is
an optional extra. Therefore no bootstrap exception is claimed. PyUnitWizard
retains its own NumPy requirement for scientific operations.

The runtime minimum and Conda recipe require ArgDigest >=0.14.0, and the
development, test, and release-gate profiles pin the public 0.14.0 release.
The downloaded `uibcdf::argdigest=0.14.0=py_0` archive has SHA-256
`983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e`,
matching the provider handoff in `uibcdf/molsyssuite#98`.

Receiving tests exercise actual quantity checking, standardization and
conversion with the published adapter. They also check that truthy values
`1`, `"yes"`, and `"False"` still digest; only literal `True` bypasses;
classmethod receivers are excluded; legacy caller identity is retained while
the optional runtime `qualname` is supplied; and a fresh-process probe
simulates absent PyUnitWizard and constructs an adapter, with its missing-dependency
diagnostic deferred to execution. PyUnitWizard's runtime configuration calls do not expose a bypass
flag or classmethod interface; these are receiving compatibility probes.

The regression-first run against 0.13 and uncorrected configuration produced
eight failures and two passes. After the correction, the configuration and
ecosystem targets passed 52 tests, and the full local Python 3.14 suite passed
688 tests with 20 skips (19 absent optional Ackredit, one intentionally
unsupported strict-JSON NaN case covered by a rejection test). Published
ArgDigest files were installed into an isolated virtual environment layered
on the existing full scientific environment; this is local receiving evidence,
not a new public PyUnitWizard artifact qualification.

A local wheel with the new runtime metadata was installed into that isolated
environment. Outside the checkout, both import orders (`pyunitwizard` first
and `argdigest` first) passed, loaded no optional unit engine during import,
accepted an unchanged alias tuple, and standardized 10 angstrom to 1 nm.
`pip check` found no broken requirements. This verifies the dependency/import
boundary; the wheel is a development probe, not a published release.

Scientific source `1a10ae9cca56b5766d09426e9964687771b6cb2a` passed
routine CI `37230831375`, policy `37230831849`, and the eight-cell
Linux/macOS Python 3.11–3.14 matrix `37230868062`. Each matrix cell
imported published ArgDigest 0.14.0 and executed 686 tests with 22 documented
skips: the local 20 plus two tests requiring sibling source checkouts.

The first release gate `37230869147` exposed a separate profile omission:
physipy and quantities were absent, although smoke, packaging and documentation
passed. `uibcdf/pyunitwizard#99` supplies those backends in the release and
development profiles. At corrected head `bd5be9e4853a3b3a8783618463ae3d641613f6c8`,
routine CI `37231386080`, policy `37231386414`, and Release Gates
`37231437144` passed. All four Python full-suite jobs executed 686 tests
with 22 documented skips; all four API/ecosystem smokes executed 16 tests;
packaging and documentation also passed. Scientific code, tests, runtime
metadata, full-matrix workflow, and matrix dependency inputs are unchanged
between these two sources, so the original eight-cell evidence remains
applicable with its original identity.

The receipt is `devguide/evidence/argdigest_014_receiving_2026-10-04.json`.
The member-local receiving implementation and applicability review are complete.
This issue remains partial only until MolSysSuite records the support-library
review as adopted in its owning inventory under `uibcdf/molsyssuite#6` and
records the version-specific receiving outcome under `uibcdf/molsyssuite#98`.
The proposed inventory evidence is the source, executed matrix and recovered
release gates above, plus the named local guard; no provider exception is needed.
