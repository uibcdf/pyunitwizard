# Implementation Patterns

Use these patterns to keep changes stable.

## 1. Boundary normalization

Normalize inputs at public API boundaries, not deep in business logic.

## 2. Explicit checks

Use explicit compatibility and dimensionality checks before conversion-sensitive operations.

## 3. Stable defaults

Configure parser/form/standards once and avoid ad-hoc runtime reconfiguration.
If a config-module resolver is used, enforce explicit precedence:
`runtime > env > file`.

## 4. Backend isolation

Keep backend-specific behavior inside `forms/*` adapters; avoid leaking it into `api/*`.

### Optional-import audit boundary

DepDigest 0.13.0 scans imports in module/class control flow, including `try`
blocks. It does not infer whether a module is reachable from package startup.
Run its raw audit from the repository root and retain the findings separately:

```bash
python -m depdigest audit --src-root pyunitwizard \
  --soft-deps ackredit,unyt,openmm,astropy,physipy,quantities --json
```

The reviewed boundary in uibcdf/pyunitwizard#93 permits six exact-file
exceptions. Each runtime adapter is imported only after its backend is requested
through `configure.load_library()` or first-demand dispatch. Module-local
backend imports initialize the types and helpers used by that adapter; moving
them into every operation would change this initialization contract. The
template is a contributor scaffold, absent from the dispatcher registry.

| Exact file | Reason for the exception |
| --- | --- |
| `pyunitwizard/forms/api_openmm_unit.py` | Requested OpenMM adapter; initializes `openmm.unit`. |
| `pyunitwizard/forms/api_unyt.py` | Requested unyt adapter; initializes its quantity/unit types. |
| `pyunitwizard/forms/api_astropy_unit.py` | Requested Astropy adapter; initializes quantity/unit types and SI dimension mappings. |
| `pyunitwizard/forms/api_physipy.py` | Requested physipy adapter; initializes units and its quantity type. |
| `pyunitwizard/forms/api_quantities.py` | Requested quantities adapter; initializes quantity/unit types. |
| `pyunitwizard/forms/template_api_form.py` | Non-dispatched scaffold with placeholder operations and an illustrative unyt import. |

Run the separately scoped audit with only these exact paths:

```bash
python -m depdigest audit --src-root pyunitwizard \
  --soft-deps ackredit,unyt,openmm,astropy,physipy,quantities --json \
  --exempt-file pyunitwizard/forms/api_openmm_unit.py \
  --exempt-file pyunitwizard/forms/api_unyt.py \
  --exempt-file pyunitwizard/forms/api_astropy_unit.py \
  --exempt-file pyunitwizard/forms/api_physipy.py \
  --exempt-file pyunitwizard/forms/api_quantities.py \
  --exempt-file pyunitwizard/forms/template_api_form.py
```

Keep the rest of `forms/` and the package in scope. New findings require review;
do not add directory exemptions or use `--allow-violations` to clear the gate.
Static results must be paired with fresh-process import regressions:

```bash
python -m compileall -q pyunitwizard
python -m pytest --receptor=llm tests/test_lazy_backend_loading.py
```

These tests block optional imports while resolving every public export and
check each requested adapter loads only its matching optional root. Run the
adapter-loading cases in the complete backend test environment. A scoped static
pass alone does not prove startup isolation or scientific correctness.

## 5. Contract tests first

For regressions or new branches, add/adjust tests before implementation changes.
