# Performance and Robustness Strategy: The MolSysSuite Consensus (March 2026)

This document outlines the agreed-upon architectural plan to optimize molecular
system processing and unit handling across **MolSysMT**, **PyUnitWizard**,
**ArgDigest**, and, where needed, **SMonitor** itself.

## 1. Motivation: The "Latency Tax" Problem

During the 1.0.0 stabilization, we identified that PyUnitWizard, while robust
and interoperable, introduced a performance bottleneck when invoked repeatedly
in high-frequency loops or recursive function calls within MolSysMT.

Our initial attempts to implement global caching within PyUnitWizard were
reverted because they interfered with complex backend protocols (e.g.,
Astropy) and dynamic state management. Since then, part of that work has been
reintroduced safely in narrower forms inside PyUnitWizard, but the broader
lesson remains: the best performance path for the ecosystem will come from a
combination of targeted core optimization and better orchestration at the API
boundaries.

The new strategy therefore moves from "aggressive internal caching" to a
**Structured Multi-Layer Offloading** model.

## 2. The Core Strategy: Triple-Layer Architecture

### 2.1 Layer 1: ArgDigest - The "Normalization Passport" (The Two-Level Pipeline)
To avoid redundant work and ensure type determinism, we implement a structured communication protocol:
- **The ValidatedPayload**: A lightweight, immutable container (`dataclass(frozen=True, slots=True)`) carrying:
    - `value`: The raw `numpy.ndarray`.
    - `unit`: The canonical unit string (e.g., 'nm').
    - `dtype`: The data type (guaranteed 'float64' for science pipelines).
    - `ndim`: The expected dimensionality of the array.
    - `is_canonical`: A boolean flag indicating the data is already in the ecosystem's standard form.
- **Contract**:
    - it is created only by trusted digestion pipelines;
    - it is consumed only by ArgDigest pipeline logic or final extractors;
    - it is a boundary object, not a persistent array wrapper to be carried
      freely through user code;
    - it is an internal ecosystem protocol, not a user-facing public quantity
      abstraction.
- **The Two-Level System**:
    1. **Semantic Internal Pipelines**: (e.g., `sci:nm_float64_payload`) These always return a `ValidatedPayload`. They are used for passing normalized data between decorated functions.
    2. **Kernel Extractors**: Specialized logic at the very end of the digestion process that unwraps the payload to deliver a naked `ndarray` to the computation kernels.

This point must stay strict: internal semantic pipelines should not sometimes
return payloads and sometimes bare arrays depending on context. The extraction
of the naked array should be a separate, explicit final step.

### 2.2 Layer 2: PyUnitWizard - Specialized "Fast-Tracks"
Generic resolvers like `standardize()` are not removed. Instead, they are
complemented in high-performance paths by explicit, "boring," and highly tested
fast-track functions:
- **Fast-Tracks**: `to_nanometers(obj)`, `to_picoseconds(obj)`, `to_kelvin(obj)`.
- **Scope**:
    - they target a small set of ecosystem-canonical units;
    - they are intended primarily for use by ArgDigest pipelines and other
      tightly controlled integration code;
    - they should accept supported quantity-like runtime objects, not become a
      second generic conversion API with broad ambiguous semantics.
- **Optimization**: These bypass general linear-algebra dimensional solvers by
  using pre-cached standard unit objects and direct type guards.

### 2.3 Layer 3: SMonitor - Aggregated Observability
Instead of per-event signals, we use aggregated diagnostics to minimize instrumentation overhead:
- **Redundancy Monitor**: A stateful counter within SMonitor that tracks cumulative redundant conversions by callsite.
- **Audit Reports**: Provides developers with a "Top-N" list of performance leaks for manual refactoring post-1.0.

This layer should be treated as part of the ecosystem design space, not as a
fixed external constraint. If a better aggregated monitor requires changes in
SMonitor, those changes are in scope.

## 3. Implementation Roadmap

1.  **Phase 1 (ArgDigest)**: Define the `ValidatedPayload` contract and the two-level pipeline logic.
2.  **Phase 2 (ArgDigest)**: Implement semantic canonical pipelines such as `sci:nm_float64_payload`, `sci:ps_float64_payload`, and `sci:kelvin_float64_payload`, plus the final extractor step for kernel-facing naked arrays.
3.  **Phase 3 (PyUnitWizard)**: Implement the first set of specialized fast-tracks (`to_nanometers`, `to_picoseconds`, `to_kelvin`).
4.  **Phase 4 (MolSysMT)**: Update critical function decorators to leverage the new semantic payloads and kernel extractors, ensuring recursive calls do not repeatedly re-enter full PyUnitWizard digestion.
5.  **Phase 5 (SMonitor)**: Integrate the aggregated redundancy monitor for final auditing.

## 4. Validation Strategy

Each phase should be accompanied by tests before rollout into the next layer.

- **ArgDigest tests**
  - `ValidatedPayload` creation and immutability.
  - semantic pipeline normalization to the expected canonical unit and dtype.
  - trusted-payload bypass behavior on repeated decorated internal calls.
  - explicit kernel extractor behavior.
- **PyUnitWizard tests**
  - correctness of `to_nanometers`, `to_picoseconds`, and `to_kelvin` across supported backends.
  - no regression in generic `convert()` / `standardize()` behavior.
  - behavior on already-canonical inputs.
- **MolSysMT tests**
  - recursive decorated call chains using the new pipelines.
  - equivalence of scientific results before and after adoption.
  - confirmation that inner kernels receive plain arrays.
- **SMonitor tests**
  - aggregation correctness.
  - no event explosion in repeated conversion scenarios.
  - reporting by callsite or equivalent useful grouping.

## 5. Expected Results

- **Stability**: Preserve the correctness and robustness already regained in PyUnitWizard, including the Astropy fixes.
- **Performance**: Substantially reduced overhead for repeated internal MolSysMT calls.
- **Maintainability**: Clearer boundaries; unit logic stays in the "digestion layer," while business logic stays in the "kernel layer."
- **Observability**: Better diagnostic visibility of redundant work without per-call event noise.

These are expected outcomes, not guarantees. They must be validated with both
microbenchmarks and real host-library scenarios.

## 6. Open Design Constraints

Before implementation starts, the following constraints should remain explicit:

- `ValidatedPayload` must stay narrow and boring. It should not turn into a
  second quantity abstraction.
- PyUnitWizard fast-tracks must remain a small, explicit set of helpers, not a
  replacement for the generic conversion API.
- The design must tolerate coordinated changes in ArgDigest and SMonitor if
  that is what the ecosystem needs.
- Performance decisions should be driven by real MolSysMT workflows, not only
  by synthetic microbenchmarks.
- Any shortcut that weakens correctness across supported backends is out of
  scope.

---
*This plan represents the current consensus between the development team and the
ecosystem maintainers for the post-hardening performance and robustness work.*
