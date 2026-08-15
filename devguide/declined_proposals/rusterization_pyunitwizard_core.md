# Proposal: Rusterization of PyUnitWizard Core for High-Performance Quantity Operations

**Status:** **declined as unnecessary (2026-08-15).** Retained as design evidence; not part of the
backlog. See "Why this was declined" below.
**Ecosystem impact:** `pyunitwizard` (fast array-unit operations), `molsysmt` (accelerated trajectory and coordinate analysis), `uibcdf` core library stack.  
**Prerequisites:** Cargo/Rust toolchain, Maturin/PyO3, Dimensional analysis crate (`uom` or custom).

The native project must not start solely to reduce Python dispatch overhead. It
may be promoted only when a representative downstream benchmark shows that
array conversion, memory transfer, or GIL contention remains a material
bottleneck after the completed Python fast-path work.

---

## Why this was declined

The condition in the paragraph above was never met, and the measurements accumulated since it was
written argue it will not be met by this reasoning.

This proposal's case, in its own section 2, rests on three costs: wrapper instantiation, runtime
unit-string parsing, and GIL overhead. The Python fast-path work has since addressed the first two
directly — see
[`completed_proposals/python_overhead_before_rusterization.md`](../completed_proposals/python_overhead_before_rusterization.md)
and [`completed_proposals/cheap_canonicity_predicate.md`](../completed_proposals/cheap_canonicity_predicate.md).
A conversion that cost 262 us when this was filed now costs **38 us**, of which **16 us is pint
doing the real work**. What a native core could contest is the remaining ~13 us of PyUnitWizard's
own dispatch, plus ~9 us of instrumentation that
[`completed_proposals/telemetry_cost_remeasured_and_signal_boundary.md`](../completed_proposals/telemetry_cost_remeasured_and_signal_boundary.md)
shows can be reduced without leaving Python.

That is the whole argument for declining: the prize is a fraction of a call whose dominant cost is
now the unit library itself, and the cheaper Python-side lever has not been pulled yet. Paying for a
Rust toolchain, a PyO3 boundary, wheel-building across the support matrix, and a second
dimensional-analysis implementation to compete for that fraction is not a proportionate trade.

Nothing here is refuted on its technical merits. Zero-copy NumPy interop and releasing the GIL
remain the right tools **if** the problem ever presents as array throughput rather than per-call
dispatch. The declining condition is specific and can be revisited: a downstream workload —
realistically a `molsysmt` trajectory loop — showing that array conversion or GIL contention, not
per-call Python overhead, is the measured bottleneck. Absent that evidence, this stays declined
rather than deferred, so it does not read as pending work.

---

## 1. Abstract

We propose the design and implementation of a native Rust-based backend extension for `pyunitwizard`, named `pyunitwizard_core`. 

While `pyunitwizard` provides a highly flexible Python facade for managing physical quantities across multiple unit engines (Pint, OpenMM, MDAnalysis), executing unit validations, unit conversions, and unit stripping on large NumPy arrays (e.g. coordinates and box vectors over trajectories) in pure Python introduces a small interpreter overhead. When called millions of times in trajectory analysis loops, this overhead accumulates into a major bottleneck.

By rusterizing the unit validation and stripping logic, we can execute dimensional checks and unit conversions at native C/Rust speed, releasing the Python GIL, and providing a fast path for downstream libraries like `molsysmt` to interact with physical quantities.

---

## 2. Why: The Python Pint/NumPy Wrapper Overhead

`pyunitwizard` wraps numerical data alongside their physical dimensions. When performing scientific calculations on coordinate arrays:
1.  **Wrapper Instantiation:** Creating quantity objects requires wrapping Python floats/NumPy arrays in a Pint class, allocating memory for wrapper metadata.
2.  **String Parsing for Units:** Parsing unit strings at runtime (e.g., `"nanometers"`, `"picoseconds"`) involves string matching and lookups.
3.  **GIL Overhead:** These operations run on Python's single thread, blocking parallel trajectory processing.

For heavy trajectory computations (e.g., RMSD, contacts, SASA), `molsysmt` is forced to "strip" units at the Rust/C boundary and re-attach them later. By having a native `pyunitwizard_core` in Rust, the unit-stripping and attachment seam can run directly in compiled code.

---

## 3. What: Rust-First Dimensional Layout

The proposed `pyunitwizard_core` will be a native Rust crate with PyO3 bindings:

```
┌────────────────────────────────────────────────────────┐
│                    Python Frontend                     │
│                  import pyunitwizard                   │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│                   pyunitwizard_core                    │
│   - Python bindings via PyO3 / Maturin.                │
│   - Fast unit stripping/validation of NumPy arrays.    │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│                  Rust Dimensional Engine               │
│   - Static dimensional types (Length, Time, Mass).     │
│   - Fast raw float conversion to standard SI units.    │
└────────────────────────────────────────────────────────┘
```

### Key Technical Pillars:
*   **Static Dimensional Analysis:** Use Rust's type system (or a compiled runtime equivalent like the `uom` crate) to represent physical dimensions (Length, Time, Angle).
*   **Zero-Copy NumPy Interop:** Use `rust-numpy` to access the memory buffers of Python NumPy arrays directly.
*   **Fast Unit Stripping:** Implement high-speed unit stripping in Rust. For example, converting a coordinate array from angstroms to nanometers will execute as a vector multiplication in C/Rust, bypassing Python loops completely.

---

## 4. How: Integration and Coexistence

To ensure 100% backwards compatibility:
1.  **Lazy Backend Dispatch:** `pyunitwizard` will use the native `pyunitwizard_core` as a high-speed engine when handling NumPy arrays and standard physical quantities.
2.  **Fallback to Pint:** For symbolic mathematics or complex/rare unit types, the system will fall back to the existing Python Pint engine.
3.  **Direct C/Rust Seam:** Downstream libraries like `molsysmt` (using `molsysmt_core` in Rust) can share unit metadata at the C-boundary, allowing `molsysmt_core` to validate and convert units in Rust before returning the coordinates to Python.

---

## 5. Prioritized Roadmap for Implementation

1.  **Phase 1 (Rust Crate Setup):** Set up the Maturin project for `pyunitwizard_core`. Implement basic dimensional structs (Length, Time, Angle, Mass) in Rust.
2.  **Phase 2 (Fast Array Stripper):** Implement high-speed array conversion and unit stripping functions for NumPy float arrays (e.g. converting `[x, y, z]` coordinates from any length unit to standard nanometers).
3.  **Phase 3 (Python Integration):** Integrate `pyunitwizard_core` into `pyunitwizard`'s core functions (`get_value`, `get_unit`, `convert`).
4.  **Phase 4 (C-Boundary Sharing):** Expose raw C-pointers for units, enabling `molsysmt`'s Rust core to query unit dimensions directly without crossing the Python GIL.
