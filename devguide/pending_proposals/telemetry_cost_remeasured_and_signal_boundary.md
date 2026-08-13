# Proposal: remeasuring the cost of telemetry, and where to put the `@signal` boundary

**Status:** proposal (2026-07-19). Everything measured on this host, with the command next to it.
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

*(I have not remeasured the DepDigest side, which section 2c also cites at 10 invocations per call.
That figure remains unverified in this document.)*

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

`benchmarks/conversion_baseline.py` already watches `get_value_nm_to_angstrom` with telemetry
disabled. **Suggestion:** add the same case with telemetry enabled, which is the mode a real user
runs in and the only one where these 10.5 us are visible.

---

## 7. Provenance

Measured on a single host: Python 3.13, x86_64, Linux 6.17, `pyunitwizard` 0.22.0, `pint` as the
default form, SMonitor on `main` after `df86d5d`. The before/after figures in section 1 were obtained
by running the same script against two SMonitor worktrees in the same session, with bare pint as a
control: it stayed at 15.6-17.3 us across every run.

One caution about the per-wrapper figures: SMonitor's microbenchmarks
(`benchmarks/signal_enabled.py`) measure a synthetic function with a single positional argument and
give ~1.24 us per wrapper. Here, with real arguments and `**kwargs`, it comes out at ~2.1 us. **The
microbenchmark underestimates the real cost by about 1.7x**; it is good for comparing before and
after, not for predicting absolutes in this repository.
