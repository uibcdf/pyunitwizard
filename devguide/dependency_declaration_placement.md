# Where backend dependencies are declared, and why not on `convert()`

**Status:** decision recorded 2026-08-15. Implemented.
**Scope:** `pyunitwizard/api/conversion.py`. No change to what PyUnitWizard requires,
reports, or enforces.

---

## The decision

`convert()` no longer carries `@dep_digest` declarations. The form-to-library table lives
in `pyunitwizard/_depdigest.py` (`LIBRARIES` and `MAPPING`), and enforcement stays where
the backend is actually imported: `digest_form()` -> `configure.load_library()`.

## What was there

Five stacked decorators, one per optional backend:

```python
@dep_digest("unyt", when={"to_form": "unyt"})
@dep_digest("openmm.unit", when={"to_form": "openmm.unit"})
@dep_digest("astropy.units", when={"to_form": "astropy.units"})
@dep_digest("physipy", when={"to_form": "physipy"})
@dep_digest("quantities", when={"to_form": "quantities"})
```

They cost **6.2 us of a 27.3 us call — 23%** — and in a `pint -> pint` conversion all five
conditions answer "no". Measured by unwrapping the decorator stack layer by layer:

| | us |
|---|---:|
| `convert()` decorated | 27.32 |
| `convert()` undecorated | 20.38 |
| the five `@dep_digest` layers | **6.24** |

About half of each wrapper's ~1.25 us is the wrapper frame itself, not its logic
(`resolve_config` is 0.091 us, the library lookup 0.077 us).

Worth noting the shape of that cost: it is **per supported backend**. Every new backend
PyUnitWizard interoperates with used to make every `convert()` call more expensive.

## Why removing them loses nothing

Checked across `pyunitwizard`, `argdigest`, `depdigest`, `smonitor` and `molsyssuite`:

| consumer | reads the declaration on `convert()`? |
|---|---|
| `func._dependencies` | written in `depdigest/core/decorator.py`, read only by DepDigest's own test of the decorator, against its own dummy function |
| `depdigest.get_info()` | no — it resolves `_depdigest.py` and reports per library. Output is byte-identical without the decorators |
| this repo's contract tests | read `_depdigest.LIBRARIES` and `MAPPING`, not decorators |
| `SHOW_ALL_CAPABILITIES` | consumed only by `LazyRegistry` (`depdigest/core/loader.py`), which this package does not use |
| AST audits, doc generation | none found |

## Why it was misplaced rather than merely redundant

`convert()` imports no backend. Every route that needs one passes through
`digest_form()`, which calls `load_library()`, which raises before the backend is touched.
Confirmed by simulating a missing `unyt`: the error that surfaces comes from
`load_library`, with its own message, not from the decorator.

So the declaration on `convert()` asserted something that was not true of `convert()` --
that it is where the dependency is consumed. The accurate statement already exists, in
the file DepDigest actually reads, and is already covered by
`test_depdigest_mapping_is_consistent_with_supported_forms`.

## What guards it now

`tests/test_depdigest_contract.py` gained two tests:

- `test_missing_backend_is_still_guarded_without_a_decorator_on_convert` simulates a
  missing backend and asserts the conversion still fails. It fails if `load_library`'s
  check is removed, so it pins the ordering the decision rests on.
- `test_convert_carries_no_per_call_dependency_wrappers` asserts only the `@signal`
  layer remains, so the declarations cannot silently return to the hot path.

## Result

| `convert(nm -> angstrom)` | before | after |
|---|---:|---:|
| telemetry enabled | 35.43 us | **29.27 us** |
| telemetry disabled | 27.36 us | **21.57 us** |
| bare pint, for reference | 15.87 us | 15.87 us |

## If `_dependencies` ever becomes real

`SHOW_ALL_CAPABILITIES` hints at a per-function capability report that does not exist yet.
If it arrives, these declarations are worth having again -- but on
`forms.load_library()`, which is where the import happens and which runs once per backend
per session rather than once per conversion.

The general fix belongs in DepDigest, not here: a single decorator resolving the required
library from a parameter through `MAPPING`, so that declaring N backends costs one wrapper
instead of N. That is filed as
`depdigest/devguide/pending_proposals/mapped_dependency_declaration.md`.
