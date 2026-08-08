# Proposal: Python overhead **before** rusterizing

**Status:** proposal (2026-07-12). **Everything measured**, with the command next to it.
**Origin:** profiling from MolSysViewer, investigating why a viewer operation cost 10 ms.
See `molsysviewer/devguide/pending_proposals/import_cost_and_lazy_loading.md`.
**Relation to [`rusterization_pyunitwizard_core.md`](rusterization_pyunitwizard_core.md):** it does
not contradict it, but it **changes its order**. Read this one first.

---

## 1. The figure that changes the priority

Measured on `puw.get_value(q, to_unit="nanometers")` (Python 3.13, pint as the default form):

| | cost | % |
|---|---|---|
| **bare pint -- the real work** | **17 us** | **7 %** |
| decorator overhead, **even when disabled** | 127 us | 49 % |
| telemetry enabled (SMonitor) | 118 us | 45 % |
| **total `puw.get_value`** | **262 us** | **15x pint** |

```bash
python -c "
import timeit, pint
from pyunitwizard import ...   # configured with pint
ureg = pint.UnitRegistry(); qp = 1.5*ureg.angstrom; qw = puw.quantity(1.5,'angstroms')
print(timeit.timeit(lambda: qp.to(ureg.nanometer).magnitude, number=3000)/3000*1e6, 'us  pint')
print(timeit.timeit(lambda: puw.get_value(qw, to_unit='nanometers'), number=3000)/3000*1e6, 'us  puw')"
```

**The computation is 7 % of the cost. The other 93 % is the layer wrapping it.**

### Why this affects the rusterization proposal

`rusterization_pyunitwizard_core.md` proposes moving validation and conversion to Rust, and places
the bottleneck in *"the Pint wrapper, unit string parsing and the GIL"*.

**If the computation were infinitely fast -- 0 us -- the call would still cost 245 us.** A **7 %**
improvement, in exchange for a Rust toolchain, PyO3, Maturin and a native core to maintain.

That does **not** invalidate rusterization: for operations on **very** large arrays (a whole
coordinate trajectory in a single call) the computation can indeed come to dominate. But the common
case in this ecosystem is not *one giant call*: it is **thousands of small ones**, and there the cost
is **fixed** -- measured, a 1000x3 array costs **the same as a scalar** (253 us vs 262 us), because
the time is not in the data, it is in the dispatch.

**Recommendation: remove the Python overhead first.** Once the call drops from 262 us to ~30 us it
can be measured again, and **then** we can decide whether the computation matters enough to
rusterize. Optimizing the 7 % before the 93 % is doing it backwards.

---

## 2. The three problems, measured

### 2a. Decorator cost -- **fixed in SMonitor and DepDigest, not here**

With SMonitor **disabled**, `puw.get_value` still costs **143 us**, against the 17 us of real work:
**the off mode costs 7.5x the computation.** The cause is that the `if not enabled` check happens
*after* the manager is built, and that DepDigest decorates itself with `@signal`.

**Those two fixes do not belong to this repository and are not documented here.** They live, with
their measurements, where they should:

- `smonitor/devguide/pending_proposals/overhead_optimization_and_profiles.md` -- the decorator's
  fast path. *(The proposal already existed; it was missing the numbers.)*
- `depdigest/devguide/pending_proposals/fast_dependency_cache.md` -- the cache, plus two defects
  that proposal did not cover: the self-decoration with `@signal` and the per-call
  `resolve_config()`.

**They are mentioned here only because the cost is paid in PyUnitWizard**, and because without them
the fixes in 2b and 2c yield far less than they could.

### 2b. PyUnitWizard enters 22 internal functions per call, **repeating work**

Profile of 100 calls to `puw.get_value`:

```
   3x  _private/forms.py:8    digest_form        <- detects the same form THREE times
   3x  _private/forms.py:38   digest_to_form
   2x  api/introspection.py   get_form
   2x  api/conversion.py:68   convert
   2x  _private/parsers.py:3  digest_parser
   ───────────────────────────────────────────
   22 internal calls to convert 1.5 A to nm
```

**This is wasted work regardless of what a decorator costs.** A quantity's form does not change
halfway through the call: detecting it three times is pure waste.

**Fix:** resolve the form and the parser **once** on entering the public function, and pass them
inward. No API change.

### 2c. The private helpers are decorated

**Twelve API functions carry `@digest` / `@signal`** (validation 2, construction 2, extraction 4,
conversion 3, context 1), and a single public call traverses them. Measured result: **4,800
invocations of SMonitor's decorator and 3,000 of DepDigest's for 300 calls** -- 16 and 10 per call
respectively.

**A `@signal` belongs to the library's public boundary, not to every helper it calls itself.**
Telemetry wants to know that the user called `get_value`, not that `get_value` called `digest_form`
three times.

**Fix:** decorate **only** the public surface. Inside, bare functions.

---

## 3. And an import problem: six backends just to declare some `TypeVar`s

`pyunitwizard/_private/quantity_or_unit.py` imports **every** installed unit backend -- pint,
openmm.unit, unyt, astropy.units, physipy, quantities -- inside `try/except`, **only to build a few
`TypeVar`s**:

```python
try:
    import unyt                                # <- drags in sympy and matplotlib
    quantity_types.append(unyt.unyt_quantity)
except:
    pass
```

A consumer using only pint (like MolSysViewer, which calls `set_default_form('pint')`) **pays all the
same**:

| | RSS |
|---|---|
| pint + openmm.unit | 146 MB |
| + unyt, astropy, physipy, quantities | 211 MB |
| **wasted, always, never used** | **65 MB** |

And it is 50 % of the time to import PyUnitWizard (`python -X importtime`): 1.70 s out of 1.93 s go
to `_private/quantity_or_unit`.

**At runtime a `TypeVar` validates nothing.** We can:

- declare them under `TYPE_CHECKING` (zero runtime cost), or
- build the list **lazily**, the first time it is asked for, or
- import **only the configured backends**.

Any of the three gives **65 MB and 1.7 s** back to the whole ecosystem.

---

## 4. What to expect from each fix

| fix | where | `get_value` goes from 262 us to... |
|---|---|---|
| decorator fast path (2a) | SMonitor | ~145 us |
| resolve the form only once (2b) | **PyUnitWizard** | ~90 us (estimate -- **measure**) |
| undecorate the private helpers (2c) | **PyUnitWizard** | ~30 us (estimate -- **measure**) |
| rusterize the computation | PyUnitWizard | -17 us off whatever remains |

**The first three are an afternoon's work and touch no API.** The fourth is a project.

The estimates in 2b and 2c are marked as such **on purpose**: they are the only figures in this
document I have not measured, because measuring them requires making the change. Everything else
carries its command next to it.

---

## 5. How to verify

```bash
# the goal: get close to pint, not to 15x pint
python -c "
import timeit
from pyunitwizard import ...
q = puw.quantity(1.5,'angstroms')
t = timeit.timeit(lambda: puw.get_value(q, to_unit='nanometers'), number=3000)/3000
print(f'{t*1e6:.1f} us   (today: 262 us | bare pint: 17 us)')"

# the import
python -X importtime -c "import pyunitwizard" 2>&1 | tail -1        # today: ~1.9 s
/usr/bin/time -v python -c "import pyunitwizard" 2>&1 | grep Maximum # goal: -65 MB
```

And `benchmarks/` plus `performance_baseline_0.20.x.json` already exist in this repository: **this
work should move their needle visibly.** If it does not, the diagnosis is wrong -- and then it is
time to measure again, not to keep optimizing.

## Implementation and results (2026-07-12)

The optimizations preceding any rusterization reach this proposal's goal:

| cumulative state | `get_value(..., to_unit="nanometers")` |
|---|---:|
| original baseline | 262 us |
| SMonitor's disabled fast path | 137.9 us |
| without DepDigest self-instrumentation | 125.8 us |
| `when` conditions without a hot `Signature.bind` | 54.1 us |
| without re-converting the already parsed unit | **28.6 us** |
| bare Pint | 17 us |

In addition, `_private/quantity_or_unit.py` no longer imports six backends to build runtime types.
The full aliases exist only under `TYPE_CHECKING`; at runtime they are `Any`. Importing that module
directly drops from **1.91 s / 217 MB** to **0.12 s / 25 MB** on this host. The adapter for an
external object is registered lazily from `get_form`, so a Pint object loads only Pint, not every
installed backend.

The last conversion improvement does not remove a validation: `_parse_unit_string` had already
produced a unit in the right `to_form`, but `convert` passed it recursively back through the public
API before using it. It is now handed over directly when the backend matches; if Matplotlib or
another client supplies a unit from a different backend, it is translated directly via
`dict_translate_unit`, without re-entering the five dependency decorators.

`benchmarks/conversion_baseline.py` includes the `get_value_nm_to_angstrom` case to watch this path.
At 28.6 us against the backend's 17 us, rusterizing stops being an answer to dispatch overhead; it
should only be reassessed for workloads where the numerical computation genuinely dominates.

With telemetry enabled and no profiling, the same call measures **64.9 us**. That is a 4x reduction
from the original 262 us, but it confirms that internal calls between functions that are also public
API still generate nested signals. Separating public wrappers from private implementations could
reduce that diagnostic cost in a later round; it is not needed for the ~30 us disabled-production
goal reached here.
