# Proposal: remeasuring the cost of telemetry, and where to put the `@signal` boundary

**Status:** proposal (2026-07-19); re-verified 2026-08-15 and reduced to a single open decision —
the public/private `@signal` split of section 4. Its section 6 benchmark task is implemented, and
section 8 reprices the decision across all nine baseline cases. Everything measured on this host,
with the command next to it.
**Origin:** performance work in SMonitor (`smonitor` on `main`, commits `023e39f` and `df86d5d`),
after which this repository's telemetry figures stopped reproducing.
**Relation to [`python_overhead_before_rusterization.md`](../completed_proposals/python_overhead_before_rusterization.md):**
it continues it. That proposal is already implemented and its results section is correct except for
one figure -- the 64.9 us with telemetry enabled -- which this document updates and explains.

---

## 1. What changed, without touching this repository

`python_overhead_before_rusterization.md` closes by saying:

> With telemetry enabled and no profiling, the same call measures **64.9 us**. [...] confirming that
> internal calls between functions that are also public API still generate nested signals.

That measurement was accurate. Measured today against the SMonitor of that moment it reproduces
**65.0 us**. But with the current SMonitor, and **with no change whatsoever in PyUnitWizard**, the
same call measures **39.5 us**:

| `puw.get_value(q, to_unit="nanometers")` | SMonitor of 2026-07-12 | current SMonitor |
|---|---:|---:|
| telemetry enabled | 65.0 us | **39.5 us** |
| telemetry disabled | 28.4 us | 29.0 us |
| cost of telemetry | 36.6 us | **10.5 us** |

The disabled path is unchanged, as it should be: that fast path was already in place. What dropped
3.5x is the **enabled** path, which is the one users run on.

### Current composition of the call (39.5 us)

| | cost | % |
|---|---:|---:|
| bare pint -- the real work | 15.6 us | 39 % |
| PyUnitWizard's own overhead | 13.4 us | 34 % |
| SMonitor telemetry | 10.5 us | 27 % |

Worth contrasting with the table opening the previous proposal: SMonitor was **45 %** of a 262 us
call. Today it is **27 %** of a 39.5 us one.

---

## 2. Two figures from section 2c that no longer reproduce

Section **2c** of the previous proposal states:

> **4,800 invocations of SMonitor's decorator** [...] for 300 calls -- 16 [...] per call.
> [...] **Fix:** decorate **only** the public surface. Inside, bare functions.

Measured today, it is **5 wrappers per call**, not 16. And -- this matters more than the number --
**all five are public API**, not private helpers:

```
1. pyunitwizard.api.extraction.get_value      <- what the user called
2. pyunitwizard.api.conversion.convert
3. pyunitwizard.api.introspection.get_form
4. pyunitwizard.parse.parse
5. pyunitwizard.api.introspection.get_form    <- a second time
```

The fix section 2c proposed -- "decorate only the public surface" -- **is already done**. What
remains is not over-decorated public surface: it is public surface **calling itself**.

That invalidates the instruction as written. Applied literally today it would mean stripping
`@signal` from `convert`, `get_form` and `parse` -- precisely the functions a user may call
directly, and we would lose their signal when they do.

*(Section 2c also cites the DepDigest side at 10 invocations per call. That figure was left
unverified when this document was written; it is now measured in section 2.1.)*

### 2.1 The DepDigest side, measured (2026-08-15)

The same correction applies to DepDigest, and in the same direction: **5 wrappers per call, not
10.** Counted on this host, exactly, via the `lru_cache` behind `resolve_config` — the `dep_digest`
wrapper consults it once per invocation, so the delta in `hits + misses` is the invocation count:

```bash
python -c "
import warnings; warnings.filterwarnings('ignore')
import pyunitwizard as puw, smonitor
from depdigest.core.config import resolve_config
puw.configure.load_library(['pint']); puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm','ps','K','mole','amu','e','kJ/mol','kJ/(mol*nm**2)'])
q = puw.quantity(1.5,'angstroms')
smonitor.configure(enabled=True, handlers=[])
used = lambda: sum(resolve_config.cache_info()[:2])
b = used()
for _ in range(100): puw.get_value(q, to_unit='nanometers')
print((used()-b)/100, 'depdigest wrappers per call')"
```

Result: **5.0 DepDigest wrappers per call** (and 4.0 SMonitor wrappers, matching this document's
post-2b figure). Measured with `pyunitwizard` 0.22.0, `depdigest` 0.10.0+2, `smonitor` 0.12.0.

**What each of those wrappers now costs.** DepDigest acted on section 2c independently: it removed
its own `@signal` self-instrumentation from the `dep_digest` wrapper and from `check_dependency`,
and it precomputes the position and default of every `when={...}` condition parameter at decoration
time instead of running `Signature.bind()` per call. Measured with
`python benchmarks/decorator_overhead.py` in that repository, on this host:

| `@dep_digest("json")`, dependency present | ns/call |
|---|---:|
| bare function | 71 |
| decorated | 592 |
| **overhead per wrapper** | **521** |
| decorated with an unmatched `when={...}` | 720 |

So DepDigest contributes roughly **2.6-3.6 us** to `puw.get_value` (5 wrappers, 0.52-0.72 us each
depending on whether the wrapper carries a condition). Against the 31.3 us telemetry-disabled path,
that is about **8-11 %** of the call — real, but an order of magnitude below the 13.4 us of
PyUnitWizard's own overhead identified in section 5. **It does not change this document's
conclusion:** the next cost block of our size is still PyUnitWizard itself, not its instrumentation
layers.

One caveat on the counting method: it measures wrapper *invocations*, which is what section 2c was
about. It does not separate the five call sites, so it cannot say whether the same public/private
self-call pattern found on the SMonitor side is also what produces these five. That question is
open, and it is the same question — if the public/private separation of section 4 is ever applied,
it would likely reduce both counts at once, since both decorators sit on the same functions.

---

## 3. The figure that most informs the decision: nothing is emitted

Across 50 calls to `puw.get_value`, **zero events** are emitted.

The 10.5 us produce no signal at all: they are the cost of *being ready* to produce one. That is the
silent case, and it is the one that dominates in any numerical loop. Any reasoning about "the
diagnostic value of these signals" has to start there: on the hot path, today, that value is zero
events and 10.5 us.

---

## 4. What is left to decide, with its price

The saving available if only the entry point stayed instrumented:

| | us |
|---|---:|
| telemetry today (5 wrappers x 2.1 us) | 10.5 |
| telemetry with a single wrapper | 2.1 |
| **saving** | **8.4 us -- 21 % of the call** |

### How to collect it without losing signals

Stripping `@signal` from `convert`, `get_form` and `parse` **would** lose signals: they are public
API. But there is a way to lose none, and it is the one the previous proposal already hinted at in
its closing -- separate the public wrapper from the private implementation:

```python
@signal
def get_form(item):
    return _get_form(item)      # public boundary: emits

def _get_form(item):            # implementation: does not emit
    ...
```

Internal callers use `_get_form`. A user calling `get_form` still generates their signal, exactly as
today. What disappears is not signal: it is the **nested repetition** of a signal for a call the user
never made.

That is precisely the criterion the previous proposal already stated:

> Telemetry wants to know that the user called `get_value`, not that `get_value` called
> `digest_form` three times.

### What it does cost

Better said before deciding than after:

- **Less precise error attribution.** Today an exception inside `get_form` called from `convert` is
  emitted with `source` pointing at `get_form`, and the breadcrumb chain shows the path. With an
  undecorated private implementation the event would be attributed to the nearest decorated wrapper.
  The exception still propagates and is still emitted; what is lost is resolution.
- **Duplicated surface.** Every public function grows a second form, and the discipline that
  internal callers use the private one has to be maintained. It is the kind of invariant that
  degrades quietly if nobody watches it.
- `get_form` is traversed **twice** per call. That is problem 2b of the previous proposal --
  repeated work -- not a decorator problem. Solving it first could make part of this discussion
  unnecessary: it would be 4 wrappers instead of 5 without touching any boundary.

**Decision (2026-08-13):** attack 2b (resolve the form only once) **before** this separation. The
string-target conversion path now preserves the already known target form instead of calling
`get_form()` on the parsed unit. Regression coverage verifies that `get_value(..., to_unit=...)`
performs one form lookup for the input quantity. Remeasure the full call afterwards, and decide then
whether the remaining overhead justifies duplicating the public surface.

Remeasured on the implementation host after this change:

| path | time |
|---|---:|
| bare Pint | 16.1 us |
| PyUnitWizard, telemetry disabled | 31.3 us |
| PyUnitWizard, telemetry enabled | 38.8 us |

The instrumented path now traverses **4 wrappers per call**, down from 5. The
remaining public/private wrapper split stays undecided because its diagnostic
attribution trade-off still needs a separate measurement-backed decision.

---

## 5. And what no longer needs fixing here

Section 2a of the previous proposal -- the cost of the decorators -- can be considered closed on the
SMonitor side. What remains per wrapper is ~2.1 us, and the design floor is around 1.2 us per
decorated call: the rest are two `ContextVar` writes that buy correct isolation between `asyncio`
tasks and threads. Going below that means giving up that isolation, and it should not be done.

In other words: **the next cost block of our size is no longer SMonitor, it is PyUnitWizard's own
13.4 us of overhead** (2b and onwards).

---

## 6. How to verify

```bash
python -c "
import warnings; warnings.filterwarnings('ignore')
import pyunitwizard as puw, smonitor, pint, timeit
puw.configure.load_library(['pint']); puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm','ps','K','mole','amu','e','kJ/mol','kJ/(mol*nm**2)'])
q = puw.quantity(1.5,'angstroms')
ureg = pint.UnitRegistry(); pq = 1.5*ureg.angstrom
us = lambda f: timeit.timeit(f, number=5000)/5000*1e6
print(f'{us(lambda: pq.to(ureg.nanometer).magnitude):5.1f} us  bare pint')
smonitor.configure(enabled=False, handlers=[])
print(f'{us(lambda: puw.get_value(q, to_unit=\"nanometers\")):5.1f} us  puw, telemetry off')
smonitor.configure(enabled=True, handlers=[])
print(f'{us(lambda: puw.get_value(q, to_unit=\"nanometers\")):5.1f} us  puw, telemetry on')"
```

Counting wrappers traversed per call:

```bash
python -c "
import warnings; warnings.filterwarnings('ignore')
import pyunitwizard as puw, smonitor
puw.configure.load_library(['pint']); puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm','ps','K','mole','amu','e','kJ/mol','kJ/(mol*nm**2)'])
q = puw.quantity(1.5,'angstroms')
smonitor.configure(enabled=True, handlers=[])
m = smonitor.get_manager(); before = m.report()['calls_total']
for _ in range(100): puw.get_value(q, to_unit='nanometers')
print((m.report()['calls_total'] - before)/100, 'wrappers per call')"
```

~~`benchmarks/conversion_baseline.py` already watches `get_value_nm_to_angstrom` with telemetry
disabled. **Suggestion:** add the same case with telemetry enabled, which is the mode a real user
runs in and the only one where these 10.5 us are visible.~~

**Done (2026-08-15), and the premise was wrong.** The benchmark was not watching anything "with
telemetry disabled": it never configured SMonitor at all, and telemetry is *enabled* by default on
import. It measured whichever ambient configuration it happened to inherit, and said so nowhere.

`run_baseline()` now pins SMonitor explicitly and times every case in both modes, emitting
`results` (enabled) and `results_telemetry_disabled`. Their difference is the instrumentation cost
per case. See section 8 for what that exposed.

---

## 7. Provenance

Measured on a single host: Python 3.13, x86_64, Linux 6.17, `pyunitwizard` 0.22.0, `pint` as the
default form, SMonitor on `main` after `df86d5d`. The before/after figures in section 1 were obtained
by running the same script against two SMonitor worktrees in the same session, with bare pint as a
control: it stayed at 15.6-17.3 us across every run.

A caution on that version string, discovered while re-verifying: `pyunitwizard/_version.py` is
git-ignored and written at build time, so `puw.__version__` reports whatever the last install wrote.
It read `0.22.0` on a checkout describing as `0.24.0-8`. The "0.22.0" above is therefore the
installed distribution, not necessarily the measured tree. Pair version strings with
`git describe --tags --always` when recording provenance.

---

## 8. Re-verification and the benchmark, 2026-08-15

Every figure in this document reproduces at `0.24.0-8`:

| | documented | re-measured |
|---|---:|---:|
| bare pint | 16.1 us | 16.5 us |
| telemetry disabled | 31.3 us | 28.9 us |
| telemetry enabled | 38.8 us | 38.2 us |
| SMonitor wrappers per call | 4 | 4.0 |
| DepDigest wrappers per call | 5 | 5.0 |

Section 3 also holds: across 50 calls only `calls_total` moves in the manager report. **Zero events
emitted.**

### What measuring every case exposed

Section 4 priced the decision on `get_value` alone. With all nine baseline cases now timed in both
modes, the instrumentation cost is far from uniform:

| case | enabled | disabled | telemetry |
|---|---:|---:|---:|
| `standardize_meter_quantity` | 492.8 us | 399.1 us | **93.7 us** |
| `get_dimensionality_quantity` | 145.8 us | 104.1 us | **41.7 us** |
| `get_value_nm_to_angstrom` | 38.5 us | 28.8 us | 9.7 us |
| `convert_nm_to_angstrom` | 39.4 us | 30.2 us | 9.2 us |
| `parse_string_quantity` | 18.2 us | 10.7 us | 7.5 us |
| `get_dimensionality_unit` | 12.5 us | 9.3 us | 3.2 us |
| `is_quantity_quantity` | 3.8 us | 1.6 us | 2.2 us |
| `parse_array_string_quantity` | 2.1 us | 0.9 us | 1.2 us |
| `get_form_quantity` | 1.5 us | 0.4 us | 1.1 us |

`standardize` carries **ten times** the absolute telemetry cost of the call this document was
written about, and `get_dimensionality` four times. Both are public functions that call other public
functions — exactly the nesting pattern of section 2 — so they traverse more wrappers per call.

This does not decide section 4, but it changes where the decision should be measured. If the
public/private split is prototyped, `standardize` and `get_dimensionality` are the cases that will
show whether it is worth the duplicated surface; `get_value` understates the prize by an order of
magnitude.

### What remains open

Only the section 4 decision, now better priced. The section 6 benchmark task is done, and the
section 2.1 question — whether the five DepDigest wrappers arise from the same public-calling-public
pattern — remains open and would likely be answered by the same prototype.

One caution about the per-wrapper figures: SMonitor's microbenchmarks
(`benchmarks/signal_enabled.py`) measure a synthetic function with a single positional argument and
give ~1.24 us per wrapper. Here, with real arguments and `**kwargs`, it comes out at ~2.1 us. **The
microbenchmark underestimates the real cost by about 1.7x**; it is good for comparing before and
after, not for predicting absolutes in this repository.
