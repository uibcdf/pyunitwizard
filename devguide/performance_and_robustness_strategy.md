# Performance and Robustness Strategy: The MolSysSuite Consensus (March 2026)

This document outlines the agreed-upon architectural plan to optimize molecular system processing and unit handling across **MolSysMT**, **PyUnitWizard**, and **ArgDigest**. 

## 1. Motivation: The "Latency Tax" Problem

During the 1.0.0 stabilization, we identified that PyUnitWizard, while robust and interoperable, introduced a performance bottleneck when invoked repeatedly in high-frequency loops or recursive function calls within MolSysMT. 

Our initial attempts to implement global caching within PyUnitWizard were reverted because they interfered with complex backend protocols (e.g., Astropy) and dynamic state management. The new strategy moves from "aggressive internal caching" to a **Structured Multi-Layer Offloading** model.

## 2. The Core Strategy: Triple-Layer Architecture

### 2.1 Layer 1: ArgDigest - The "Normalization Passport" (The Two-Level Pipeline)
To avoid redundant work and ensure type determinism, we implement a structured communication protocol:
- **The ValidatedPayload**: A lightweight, immutable container (`dataclass(frozen=True, slots=True)`) carrying:
    - `value`: The raw `numpy.ndarray`.
    - `unit`: The canonical unit string (e.g., 'nm').
    - `dtype`: The data type (guaranteed 'float64' for science pipelines).
    - `ndim`: The expected dimensionality of the array.
    - `is_canonical`: A boolean flag indicating the data is already in the ecosystem's standard form.
- **The Two-Level System**:
    1. **Semantic Internal Pipelines**: (e.g., `sci:nm_float64_payload`) These always return a `ValidatedPayload`. Used for passing data between decorated functions.
    2. **Kernel Extractors**: Specialized logic at the very end of the digestion process that unwraps the payload to deliver a naked `ndarray` to the computation kernels (JIT/Numba friendly).

### 2.2 Layer 2: PyUnitWizard - Specialized "Fast-Tracks"
Generic resolvers like `standardize()` are replaced in high-performance paths by explicit, "boring," and highly tested fast-track functions:
- **Fast-Tracks**: `to_nanometers(obj)`, `to_picoseconds(obj)`, `to_kelvin(obj)`.
- **Optimization**: These bypass general linear-algebra dimensional solvers by using pre-cached standard unit objects and direct type guards.

### 2.3 Layer 3: SMonitor - Aggregated Observability
Instead of per-event signals, we use aggregated diagnostics to minimize instrumentation overhead:
- **Redundancy Monitor**: A stateful counter within SMonitor that tracks cumulative redundant conversions by callsite.
- **Audit Reports**: Provides developers with a "Top-N" list of performance leaks for manual refactoring post-1.0.

## 3. Implementation Roadmap

1.  **Phase 1 (ArgDigest)**: Define the `ValidatedPayload` contract and the two-level pipeline logic.
2.  **Phase 2 (PyUnitWizard)**: Implement the first set of Specialized Fast-Tracks (nm, ps, K).
3.  **Phase 3 (MolSysMT)**: Update critical function decorators to leverage the new semantic payloads, ensuring recursive calls skip PyUnitWizard.
4.  **Phase 4 (SMonitor)**: Integrate the aggregated redundancy monitor for final auditing.

## 4. Expected Results

- **Stability**: Elimination of `RecursionError` by avoiding circular introspection in complex backends.
- **Performance**: Near-zero overhead for internal MolSysMT calls.
- **Maintainability**: Clearer boundaries; unit logic stays in the "digestion layer," while business logic stays in the "kernel layer."

---
*This plan represents the consensus between the development team and the ecosystem maintainers for the 1.0.0 release cycle.*
