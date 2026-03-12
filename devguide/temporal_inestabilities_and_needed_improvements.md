# Temporal Instabilities and Needed Improvements (March 2026)

This document records what was initially suspected, what was later confirmed as
real, what has already been corrected in `main`, and which optimization ideas
remain open only as optional future work. It is intended to be the working
checkpoint we can share with MolSysMT to gather feedback about real host-library
needs before deciding whether further changes are justified.

It should not be read only as a bug ledger. It also captures the current
architectural intention behind PyUnitWizard:

- PyUnitWizard should be a strong interoperability layer for scientific Python
  quantities;
- it should serve both library developers embedding units support in their APIs
  and end users composing scientific workflows across libraries;
- performance work should therefore be evaluated not only in isolation inside
  PyUnitWizard, but also in terms of how it affects host-library integration,
  debuggability, and the user experience of working with quantities naturally.

## 1. Executive Summary

The critical issues that motivated this document were real, but they were not
all of the same kind.

Some were correctness bugs and had to be fixed before anything else:

- Astropy recursion caused by incorrect value extraction.
- String conversion paths that could skip parsing and return raw strings.
- Parser-dependent parse caching.
- Standardization prebuild logic placed in the wrong part of configuration.

Others were optimization opportunities rather than blockers:

- dimensionality caching,
- standard lookup caching,
- faster introspection shortcuts,
- reduction of avoidable internal probe-miss overhead.

The work done since then confirms a pattern that matters for future decisions:

- correctness fixes were necessary and paid off immediately;
- some targeted caches were worth implementing because they were simple and
  semantically safe;
- other ideas remain plausible, but are still not justified without stronger
  benchmarks or host-library pressure from MolSysMT.

Just as important, the current work has clarified that "optimization" is not a
single thing here. We need to distinguish between:

- optimization of PyUnitWizard internals;
- guidance for how host libraries should use PyUnitWizard at their API edges;
- and the long-term goal of making quantity interoperability feel natural to
  users who already think in terms of NumPy, pandas, matplotlib, and domain
  libraries rather than in terms of PyUnitWizard internals.

## 2. What Was Confirmed As Real

Before detailing each issue, it is worth stating explicitly that this work did
not happen in isolation. Much of the motivation came from MolSysMT's attempt to
reduce the units-handling latency paid in repeated scientific workflows, such as
trajectory processing or large-scale argument validation.

That earlier work explored four main ideas:

- faster form introspection through type caching;
- no-op fast paths in `convert()` when no real conversion was needed;
- string parse caching;
- pre-calculation of standardization algebra.

The right lesson from that earlier exploration is not that those ideas were
mistaken. The better lesson is that some of them were implemented too
aggressively, with insufficient state hygiene, or without a sufficiently narrow
semantic scope.

### 2.1 Astropy Recursion Was a Real Production Bug

This was the most serious issue found in this round.

The root cause was precise:

- `astropy.units.Quantity` is a subclass of `numpy.ndarray`;
- `pyunitwizard.api.extraction.get_value()` had a fast path using
  `isinstance(quantity, np.ndarray)`;
- Astropy quantities were therefore treated as raw NumPy arrays instead of as
  backend quantities;
- downstream code such as `pytest.approx` and NumPy scalar checks then entered a
  recursive path while trying to interpret the object.

This bug was serious not only because tests failed, but because it plausibly
explains the RAM and swap exhaustion observed while running the affected tests.

Status:

- confirmed real;
- corrected in `2fec9f9` (`fix(extraction): avoid ndarray fast path for astropy quantities`);
- covered with regression tests in `tests/test_get.py`.

### 2.2 Cross-Backend Failures With Astropy Were Real, But Secondary

The failing Astropy integration tests and frontend cross-backend matrix tests
were not independent mysteries. They were largely symptoms of the same faulty
value-extraction path described above.

Once the Astropy extraction issue was fixed, the following test areas returned
to green:

- `tests/astropy_units`
- `tests/integration/test_frontend_cross_backend_matrix.py`
- `tests/integration/test_backend_interop_matrix.py`

Status:

- confirmed real;
- resolved as an effect of the Astropy extraction fix.

### 2.3 String Fast Paths In `convert()` Were Wrong

This was also a real bug.

The problem was conceptual: strings are not already-converted runtime quantities,
so they must stay on parser-controlled paths until they become proper backend
objects.

The incorrect behavior was that some string inputs could bypass parsing and
return unchanged as raw strings, depending on the target arguments and the
active defaults.

Status:

- confirmed real;
- corrected in `d4c0362`
  (`fix(parse): keep string conversions on parser-controlled paths`);
- regression coverage added in `tests/test_conversion_branches.py` and
  `tests/test_parse.py`.

### 2.4 Parse Caching Was Too Dependent On Global Runtime State

This was not just a performance detail. It had correctness implications.

The issue was that `parse()` could cache results while the effective parser was
still being inferred from runtime state. That made the cache key weaker than the
real semantics of the operation.

This was especially fragile in mixed contexts where the default parser changed
or when Astropy parsing entered routes it was not ideal for, such as certain
array-like quantity strings.

Status:

- confirmed real;
- corrected in `d4c0362`;
- parser resolution now happens before the cached path is used.

## 3. Optimizations That Were Worth Implementing

These improvements were not emergency bug fixes, but after inspection and
benchmarking they were simple enough and safe enough to justify entering `main`.

Several of them correspond directly to ideas that had already been explored from
the MolSysMT side. The current conclusion is therefore not that the earlier
optimization search was wrong. It is that some parts of it could be recovered in
a stricter and safer form.

### 3.1 Standardization Matrix Prebuild

The original idea was good: `get_standard_units()` should not rebuild least-
squares support structures repeatedly when the configured standard units have
not changed.

What was wrong initially was not the idea, but the placement of the first local
implementation. The prebuild had been inserted too early in `set_standard_units()`,
inside a loop, which made the configuration flow harder to reason about.

That was corrected by moving the prebuild to the end of configuration, once the
standard-unit state was already complete.

Status:

- worth implementing;
- corrected and stabilized in `914ad5a`
  (`perf(standardization): prebuild standards matrices after configuration`);
- reset hygiene added as part of the same consolidation.

Why it was worth it:

- low conceptual risk;
- directly tied to repeated standardization work;
- easy to invalidate cleanly on `configure.reset()` and `set_standard_units()`;
- it recovers, in a cleaner form, part of the earlier pre-calculated algebra
  strategy explored for MolSysMT integration.

### 3.2 Type-to-Form Cache Hygiene

The `_TYPE_TO_FORM_CACHE` already existed, so the relevant question was not
whether to add it, but whether its lifecycle was safe.

Clearing it on `configure.reset()` was a small but correct hardening step.

Status:

- worth implementing;
- corrected in `2c61b1f`
  (`fix(introspection): clear type-form cache on reset`).

Why it was worth it:

- very small change;
- obvious reset semantics;
- removes unnecessary state persistence across tests and runtime resets.

### 3.3 Direct Backend Detection For Common Forms

This optimization added fast explicit detection for common backends based on the
object type string before falling back to slower dispatch checks.

Status:

- worth implementing;
- added in `eb27de1`
  (`perf(introspection): add direct backend detection for common forms`).

Why it was worth it:

- low risk;
- fully internal;
- improves a very hot path (`get_form()`);
- it shows that the original "instant introspection" direction was sound in
  principle, even if the first broader attempt interacted badly with Astropy.

### 3.4 Dimensionality Cache By Canonical Unit

This was one of the optional ideas originally considered speculative. After
measuring the cost profile, it became reasonable to implement in a constrained,
safe form.

The chosen design was intentionally conservative:

- cache key: `(form, canonical unit string)`;
- cached value: dimensionality dictionary;
- returned values are copied so callers cannot mutate the cache accidentally;
- cache cleared on `configure.reset()`.

Status:

- worth implementing;
- added in `7da1bfe`
  (`perf(introspection): cache dimensionality by canonical unit`).

Why it was worth it:

- conceptually simple;
- clear invalidation point;
- directly benefits repeated validation and standardization flows.

This is also where one earlier engineering lesson needs refinement. The real
issue is not simply that "global caches are dangerous". The more accurate lesson
is that global caches are dangerous when their keys are semantically weak or
their invalidation boundaries are unclear.

Remaining caution:

- if future backends expose unit-string identities that are not stable enough,
  the key design may need refinement.

### 3.5 Standard Lookup Cache By Dimensionality

After the dimensionality cache, the next reasonable optimization was caching the
resolved standard unit for a dimensionality already seen under the current
configuration.

Again, the implemented form was intentionally narrow:

- cache key: tuple of exponents in `kernel.order_fundamental_units` order;
- cache value: canonical configured standard-unit string;
- cache cleared on `configure.reset()` and every `set_standard_units()`.

Status:

- worth implementing;
- added in `ed20378`
  (`perf(standardization): cache resolved standards by dimensionality`).

Why it was worth it:

- cheap and deterministic;
- tied to configured standards, so invalidation is explicit;
- gave measurable improvements in repeated `standardize()` workloads;
- it recovers another part of the earlier MolSysMT performance intent, but in a
  form that is easier to reason about and reset safely.

### 3.6 Avoiding Internal Probe-Miss Overhead

Profiling showed that some internal core paths were calling public
`is_unit()` logic even when the object form was already known. That is not a
correctness bug, but it is wasteful because `is_unit()` is designed for public
probing, including debug emission on misses.

Using direct backend checks in those internal paths preserved the public probe
behavior for real user-facing misses while removing unnecessary cost from hot
internal flows.

Status:

- worth implementing;
- added in `25b60bd`
  (`perf(core): avoid probe misses in internal unit checks`).

Why it was worth it:

- it reduced noise and overhead without changing the public semantics of
  `is_unit()` itself;
- it improved both `get_dimensionality()` and `standardize()`.

## 4. Measured Effect Of The Optional Optimizations

The benchmark work added under `benchmarks/` was useful because it prevented us
from optimizing blindly.

The most relevant observations were:

- after the correctness fixes, `standardize()` became the clearest remaining
  hotspot among the small PyUnitWizard core operations we were measuring;
- string parsing and `get_form()` were not the dominant costs anymore;
- after the later optimizations, short-baseline measurements showed a reduction
  of `standardize_meter_quantity` from roughly `1.16e-3` s to roughly
  `8.3e-4` s;
- `get_dimensionality_quantity` also improved materially after the cache and the
  internal probe-miss cleanup.

These are microbenchmark numbers, so they should not be overinterpreted as
application speedups. Still, they were sufficient to justify the implemented
changes.

## 5. What We Considered And Did Not Implement

Some ideas remain valid in principle but did not yet clear the bar for entering
the codebase.

### 5.1 Unit String Caching

This still looks plausible for workloads that repeatedly rebuild units from the
same strings, but it is not clearly the next bottleneck anymore.

Why it was not implemented:

- benchmark evidence is still not strong enough;
- cache-key semantics get trickier when aliases, parser differences, and unit
  normalization enter the picture;
- the risk of introducing subtle parser-state bugs is higher than with the
  caches that were implemented.

Current judgement:

- possibly useful later;
- not justified yet.

This corresponds directly to one of the optimization pillars explored earlier
for MolSysMT. The present view is not that it was a bad idea, but that it still
needs stronger evidence from real workloads before it is worth the added
complexity.

### 5.2 More Aggressive Introspection Caching

We already hardened and improved introspection, but there is still a question of
how far to go.

Why we stopped where we did:

- current gains were already good;
- more aggressive caching can become brittle if backend classes, lazy imports,
  or runtime registration patterns change;
- the remaining visible cost is increasingly in wrappers and instrumentation,
  not in simple form detection.

Current judgement:

- possible future work;
- not obviously the best next use of effort.

### 5.3 Numba Or Similar Low-Level Acceleration

This idea is still not attractive here.

Why it was not implemented:

- the hot paths are not dominated by numeric loops that would benefit naturally
  from JIT compilation;
- the cost is in dispatch, wrappers, parsing, compatibility checks, and backend
  calls;
- the added maintenance burden is not justified.

Current judgement:

- not recommended.

## 6. What Still Looks Uncertain

The main remaining uncertainty is no longer about correctness. It is about
where PyUnitWizard should stop and where host-library integration strategy
should begin.

### 6.1 Instrumentation Overhead vs Observability Value

Profiling now shows that a meaningful fraction of residual overhead comes from:

- `smonitor` wrappers,
- `depdigest` wrappers,
- generic wrapper machinery such as `inspect.bind()` and default application.

This is not necessarily a problem. Observability and dependency diagnostics are
part of the value of the micro-ecosystem. The question is whether some internal
PyUnitWizard paths should have a lighter-weight internal route while preserving
the public instrumentation contract.

Why this remains open:

- the answer depends on how much MolSysMT and related libraries value the
  current observability;
- it is an architecture decision, not just a micro-optimization;
- if we introduce lighter-weight internal fast paths, we must do so without
  weakening the public diagnostic contract that makes the ecosystem easier to
  understand and debug;
- and if the best solution requires coordinated changes in `smonitor` or
  `argdigest`, that should be considered acceptable rather than treated as out
  of scope.

### 6.2 Host-Library Usage Patterns

We still need clearer evidence from real host libraries, especially MolSysMT,
about where PyUnitWizard actually sits in hot paths:

- mostly API-edge normalization?
- repeated argument validation?
- repeated standardization of small quantities?
- user-facing scripting with transparent frontend mode?

Without that, it is easy to overfit the optimization work to microbenchmarks.

### 6.3 Core Optimization vs Ecosystem Strategy

Another open question is where future effort should be spent.

It is possible to continue optimizing PyUnitWizard internally, but there is a
point at which the more important gains may come instead from giving host
libraries clearer usage patterns, for example:

- standardize once at the API boundary;
- validate and normalize quantities before entering repeated kernels;
- move inner numeric work onto plain arrays in canonical units;
- preserve rich quantity objects mainly at user-facing and integration-facing
  layers.

This matters because the strategic goal is not just to make PyUnitWizard faster
in isolation. The broader goal is to make it a reliable units layer for the
scientific Python ecosystem.

This is exactly where the MolSysMT offloading lesson still stands. In many host
libraries, the biggest practical win may still come from normalizing once at the
API boundary and letting inner kernels operate on plain arrays in canonical
units.

### 6.4 User Experience Still Matters Alongside Performance

We should also keep explicit that PyUnitWizard is not only for library authors.
Part of its value is enabling users to move between libraries while continuing
to think in natural quantity objects.

That means future decisions should consider not only:

- whether a change speeds up a microbenchmark,

but also:

- whether it preserves predictable behavior across supported backends;
- whether it helps users write scripts that combine multiple scientific
  libraries coherently;
- whether it keeps the mental model of quantities simple for both developers and
  scientists.

## 7. Guidance For MolSysMT Feedback

This document should now be used to ask concrete questions, not only to collect
opinions.

The most useful feedback from MolSysMT would be:

- whether Astropy-heavy workflows are now behaving correctly in real use;
- whether PyUnitWizard is mostly used at API boundaries or inside repeated inner
  workflows;
- whether `standardize()` remains a noticeable cost in realistic MolSysMT
  scenarios;
- whether the current `smonitor` / `depdigest` visibility is considered worth
  its overhead;
- whether repeated construction from strings is common enough to justify unit-
  string caching later.

The most useful qualitative feedback would also be:

- whether MolSysMT sees PyUnitWizard primarily as an internal implementation
  detail or as a strategic interoperability layer;
- whether future work should prioritize lower internal overhead or stronger
  cross-library ergonomics for end users;
- whether the current instrumentation depth is helping real development enough
  to justify its runtime cost;
- whether the balance has now changed in practice, or whether the main answer
  still remains "use PyUnitWizard less often inside hot paths".

## 8. Practical Conclusion

The original urgent instabilities have been addressed.

The Astropy bug was real and serious, and it is now fixed. The parser and string
conversion issues were also real, and they are fixed. The standardization and
introspection cleanup work was worth doing and has already produced measurable
benefit.

What remains is no longer emergency stabilization work. It is a more strategic
question:

- which additional optimizations are actually needed by host libraries;
- which costs are acceptable because they buy observability and integration
  diagnostics;
- and whether further work should focus on PyUnitWizard itself or on how
  libraries such as MolSysMT use it at their API boundaries.

In other words, the next stage should not be driven by optimization for its own
sake. It should be driven by the kind of units layer we want PyUnitWizard to be
for the broader scientific Python ecosystem.

The refined position after this round of work is therefore:

- the MolSysMT offloading strategy was and remains correct;
- PyUnitWizard should still become faster where it can do so safely;
- and if ecosystem-wide improvement requires coordinated changes across
  PyUnitWizard, `argdigest`, and `smonitor`, those changes should be considered
  part of the same engineering problem rather than treated as separate worlds.
