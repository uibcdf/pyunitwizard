---
summary: Evaluate QuantityRecord as a backend translation hub.
issue: uibcdf/pyunitwizard#106
status: resolved
opened: 2026-10-04
closed: 2026-10-22
verification: measured
area: [serialization, interoperability]
guard: tests/test_record_translation_benchmark.py
normative: benchmarks/README.md
blocked_by: []
supersedes: []
---

# Evaluate QuantityRecord as a backend translation hub

What — Separate the deferred translation-hub evaluation from the design record #83 and MVP #82.

How — Measure selected real backend-to-backend pipelines against current translators. Evaluate whether SI descriptors can support independently useful translators without duplicating unit semantics or silently changing registry definitions; retain explicit dimensional/kind and affine checks.

Why — The design discusses reducing pairwise translators to one hub, but current record construction/read-to-quantity still uses Pint. The implemented inert storage form does not establish a Pint-independent translation hub.

Acceptance — Provide numerical/parity/definition-conflict tests and performance/maintenance evidence for a real workflow; identify precisely which dependencies and conversions disappear. Preserve existing signatures and scientific behavior. Implementation or deferral must follow evidence; no automatic replacement of current dispatch.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.

## Evaluation plan — 2026-10-22

Use the published TopoMT coordinate fixture already retained in this repository
as a concrete molecular-data boundary. Compare public direct conversion,
live quantity to freshly sealed record to target, and an already-stored record
read to target. Do not compare the last case as if it paid the writer's cost.
Measure warmed repeats with telemetry explicitly enabled and disabled; retain
raw samples, source/input hashes and actual runtime/provider versions. Add parity,
affine, field/kind, tamper and conflicting-registry checks before timing.

An initial OpenMM-to-unyt angstrom probe fails because the existing translator
passes symbol `A` to unyt as amperes. Track and fix that separately before using
the route as performance evidence; a translator bug is not justification for a
new hub. No new record format, dispatch replacement or Pint-removal claim is
authorized by the evaluation alone.

The sequential pre-correction measurements also find an unyt→Astropy outlier:
its adapter calls `to_pint()` without the shared registry, causing construction
on every conversion (separately owned by #122). Add a live via-Pint control and
remeasure after that fix. The record path must not receive architectural credit
for avoiding a removable translator allocation. Before/after measurements retain
their own tool/source hashes and cost scopes.

## Decision — evaluation complete, no hub replacement

Keep live backend conversion on its direct translators and existing Pint bridge.
Do not introduce QuantityRecord construction/sealing as an intermediate for every
live conversion. Keep records at verified interchange/storage boundaries, where
their field/kind/definition checks and seals are the required work. The evaluation
and reusable measurement operation are delivered; this closes an **evaluation**,
not implementation or stable admission of a Pint-independent translation hub.

Two local translator defects explain actionable improvements without replacing
dispatch: #120 fixes OpenMM angstrom/current confusion by reusing semantic
translators; #122 removes repeated Pint registry construction from unyt→Astropy.
The latter adapter was already using Pint, but omitted the shared registry.
Both have independent archived reports, regression tests and a pre-publication
provider notice in uibcdf/molsyssuite#127. No client copies were edited.

## Workload and method

Real input: `tests/data/topomt_quantity_records.json`, the published TopoMT
coordinates from `uibcdf/topomt@bfbd28f8c3d25a438c7b3d1e526097dd56f63d3c`,
shape 72×3, float64, in angstrom. This establishes real input provenance, not
production adoption of each selected backend pair. A second input tiles that
array 1000 times to 72000×3; it is a synthetic size control, not evidence of
growing trajectories. A float32 Celsius→kelvin array is an affine control.

The reusable owner operation is
`devtools.benchmark_record_translation.compare_translation`. The CLI and its
cost scopes are documented in `benchmarks/README.md`. It checks target unit,
numeric parity, shape and dtype against an explicit Pint reference before and
after timing; no universal unit oracle is claimed. It retains seven raw samples
per route/mode, rotates route order, pins telemetry on/off and restores policy
and telemetry enabled state on failure. Optional attribution capture is absent.
Imports, setup, wire encoding, reference/parity checks and profiling are excluded.

The before source is `0734c1467c0d747eccf19bd7bd6a19f548ab1e32`; the final
measured source is `af2f1b0234067b71d65839670f6c96279d79b686`. Both are clean
source checkpoints, separately hashed with their input and tool bytes. The before
tool had four routes; final evidence adds the live Pint control. Before runs use
10 iterations/sample, final real/synthetic runs use 100/20. This is not a paired
installed-artifact qualification or a portable speedup promise. An accidentally
overlapping initial pair was interrupted and discarded; only completed sequential
runs appear in [the raw receipt](../evidence/record_hub_2026-10-22.json).

## Results

Medians in microseconds per operation, telemetry enabled, final measured source:

| Real input route (72×3) | Direct | Live via Pint | Fresh record → target | Existing record → target | Wire → verify → target |
|---|---:|---:|---:|---:|---:|
| Pint → OpenMM | 59.75 | 105.21 | 374.44 | 141.87 | 309.12 |
| OpenMM → unyt | 260.35 | 276.29 | 553.05 | 286.73 | 469.10 |
| unyt → Astropy | 138.67 | 184.35 | 434.86 | 135.06 | 306.96 |
| Celsius → kelvin, Pint → unyt (control) | 222.99 | 277.84 | 542.71 | 310.33 | 467.77 |

| Synthetic input route (72000×3) | Direct | Live via Pint | Fresh record → target | Existing record → target | Wire → verify → target |
|---|---:|---:|---:|---:|---:|
| Pint → OpenMM | 498.33 | 498.15 | 6651.70 | 705.32 | 13171.25 |
| OpenMM → unyt | 433.90 | 423.49 | 6618.62 | 632.81 | 12737.46 |
| unyt → Astropy | 621.41 | 567.41 | 6644.09 | 594.98 | 12873.41 |

The fresh-record route costs 2.12–6.27 times direct conversion for the small
coordinate arrays and 10.69–15.25 times for the tiled input. Disabled-telemetry
ratios are 2.16–7.68 and 11.08–16.30 respectively; raw samples, including the
affine control, are retained. Small differences between a pre-existing record
reader and a direct live conversion do not establish producer-cost elimination.
The reader starts from an already immutable, validated record; wire verification
and fresh construction remain separately measured work.

Before #122, the unyt→Astropy direct medians were 275672.62 µs (small) and
225394.40 µs (large); after registry reuse they are 138.67 and 621.41 µs.
The deterministic regression forbids the allocation itself. Timing differences
also include the documented tool/order/sample-count change, so the allocation
test, source diagnosis and separately profiled calls establish the mechanism,
rather than a claim of universally repeatable timing ratios.

## Dependencies, semantics and maintenance

No required dependency or backend translation disappears. Separately profiled
unyt→Astropy operations show direct conversion using unyt's shared-Pint helper
and Pint's Astropy translator once each. The fresh-record route uses both too,
plus `_to_pint`, `_seal`, `_registry`, construction and reading. Stored-record
readers still construct a Pint quantity and use Pint's target translator.
The existing dispatcher already synthesizes missing live translators through
Pint; a sealed-record intermediate does not reduce that adapter boundary.

The standard-library reference reader proves verified numeric SI reading is
possible without Pint. It does not establish target object construction, canonical
name/definition agreement, quantity-kind semantics or general affine behavior
across registries. A new independent hub would need those owner contracts and
conformance tests; bypassing the current cross-checks is not an optimization.
This evaluation does not prove that such a future design is impossible.

Numerical and failure checks include float32 affine behavior, the real coordinate
fixture across three backend pairs, a broken-translator negative control, foreign
Pint definition conflicts, field/kind handshakes and the existing tamper tests.
These are informative cases, not every optional backend/registry/unit combination.
In particular, arbitrary custom non-Pint registries are not qualified by this work.

Keeping direct conversion also avoids coupling all live operations to provisional
qrec storage format/version changes, seals and copy costs. A future re-evaluation
needs a measured consumer requiring a missing Pint-independent operation or a
material live conversion cost that local translator reuse cannot remove. It must
state exactly which dependency/semantic obligation disappears. This record does
not authorize a new format or change stable/provisional scope.

## Validation and remaining work

Local Python 3.14.7: 859 full-suite tests pass, one expected JSON/NaN skip and
one existing deprecation warning. The network-enabled installed-consumer test
and temporary physipy 0.2.8/quantities 0.16.4 overlay are documented in #120/#122;
the shared environment is unchanged. Ruff passes repository-wide (213 files),
and the owned-copy Sphinx build has zero warnings. The benchmark regression guard
requires complete cost scopes and correct output, refuses false parity, and
checks restoration on clock failure; existing record tests cover tamper and
handshake semantics. Final exact-head native gates belong in the issue closeout.

Installed metadata and editable development providers are recorded separately
from source hashes. No clean public artifact, other interpreter/platform, new
provider admission or client migration is claimed. Public 0.28.1 retains its
original source/file and does not contain these later corrections.

#121 separately tracks the older conversion-baseline script's literal Python
3.13 provenance; this evaluation records actual Python 3.14.7. #105 still needs a
measured growing-data consumer; neither a tiled benchmark nor a static TopoMT
snapshot supplies one. It remains open without speculative append implementation.
