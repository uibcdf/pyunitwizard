---
summary: Document exact-file optional-import audit exceptions with startup guards.
issue: uibcdf/pyunitwizard#93
status: partial
opened: 2026-10-04
closed:
verification: measured
area: [dependencies, adapters, testing]
guard: tests/test_lazy_backend_loading.py::test_public_imports_do_not_attempt_optional_backend_imports
normative: docs/content/developer/implementation-patterns.md#optional-import-audit-boundary
blocked_by: []
supersedes: []
---

# Optional-backend audit boundary

## What

DepDigest 0.13.0 reports eleven optional imports: one in the contributor template
and ten in five runtime adapters. A template-only exemption leaves ten findings.
Static eager-scope findings do not establish that package startup reaches those
modules. PyUnitWizard owns this boundary decision under uibcdf/pyunitwizard#93;
provider release and central coordination remain uibcdf/depdigest#29 and
uibcdf/molsyssuite#95.

## How

Keep the scaffold in place and document six exact-file exceptions: the template
plus the requested OpenMM, unyt, Astropy, physipy and quantities adapters. Their
backend imports initialize module-local types and helpers after first demand.
The template is absent from the adapter registry. The maintained rationale and
raw/scoped commands live in `docs/content/developer/implementation-patterns.md`.
No directory exemption, automatic allow-violations mode, dependency upgrade or
mandatory CI audit job is introduced.

Pair the static audit with syntax compilation and subprocess regression tests.
One fresh process blocks all six optional roots while importing PyUnitWizard
and resolving every public export; caught import attempts also fail the test.
Five additional fresh processes request individual adapters and assert that
only the requested optional root is imported, the registry contains only that
backend, and the template remains unimported.

## Why

The dispatcher already supplies the delayed import boundary. Moving every
backend import inside every operation would require a wider adapter rewrite,
including annotation/type initialization and Astropy dimension mappings,
without addressing a demonstrated startup leak. Exact-file exceptions retain
the established initialization contract while all other source files stay
audited and fresh-process tests guard reachability and backend isolation.

## What is measured and what is assumed

The raw audit on this working source returns eleven findings and exit 1 using
the published Conda file `depdigest-0.13.0-py_0.tar.bz2`, SHA-256
`e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`.
The scanner is loaded directly from its existing extracted package cache in the
Linux/Python 3.14.7 test environment; this does not upgrade that environment's
installed DepDigest 0.11.0. The separate runtime tests use the installed provider.

The separate scoped audit returns zero findings and exit 0 with the six exact
file exceptions; the template-only audit still returns ten findings and exit 1.
The raw, template-only and scoped payloads, published artifact identity and
Python-source-tree digest are preserved separately in
`devguide/evidence/optional_backend_audit_2026-10-04.json`. The receipt identifies
the base commit and explicitly describes the uncommitted candidate, rather than
claiming the base commit already contains the fix.

Syntax compilation passes. All seven fresh-process adapter tests pass as part
of the focused parsing/comparison/import run (42 tests) and the complete parallel
suite (661 passed, 20 documented skips). Ruff checking and formatting pass for
the changed executable files. Existing provider measurements on older snapshots
remain dated evidence; a prior template-only pass is not a current scoped pass.

## What was refuted

The newer raw findings are not removed by exempting the template alone. They
also do not prove a root-import leak: fresh-process guards pass in the complete
backend test environment.

## Scope and exclusions

Exceptions cover only the six named files and their requested-module boundary.
They do not grant exceptions to new adapters or imports in other package files,
certify arbitrary dynamic imports, or qualify public PyUnitWizard artifacts.

## Acceptance criteria

- Preserve raw and exact-file-exempted audit results separately.
- Document each adapter's import boundary and keep all remaining files in scope.
- Pass syntax and fresh-process public/individual-backend import checks.
- Review/commit the maintained decision and tests, then synchronize issue closure
  and archive this record without deleting its evidence.

## Dependencies and risks

Static audits cannot model dynamic module reachability. The subprocess guards
complement the scanner, and new imports or changes to adapter loading require a
new boundary review. Broad provider runtime adoption is a separate decision.
