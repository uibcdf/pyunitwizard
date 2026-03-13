# Performance and Robustness Strategy: The MolSysSuite Consensus (March 2026)

This document outlines the agreed-upon architectural plan to optimize molecular
system processing and unit handling across **MolSysMT**, **PyUnitWizard**,
**ArgDigest**, and, where needed, **SMonitor** itself.

This document now serves two purposes:

- it records the intended architecture;
- it reports the result of the first implementation wave, so the other team can
  react to what actually worked in code rather than only to a design sketch.

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

Implementation status:

- implemented in `argdigest` as `ValidatedPayload`;
- implemented semantic canonical pipelines for:
  - `nm_float64_payload`
  - `ps_float64_payload`
  - `kelvin_float64_payload`
- implemented explicit extractor:
  - `unwrap_validated_payload`

Practical note from implementation:

- the payload-and-extractor model works;
- however, for MolSysMT the most natural place to apply the policy was not in
  public functions but in caller-aware digesters under
  `molsysmt/_private/arg_digestion/argument/*`.
- in this first wave, the most practical win inside MolSysMT has come less from
  carrying payloads deeply through the whole call graph and more from using the
  payload idea to justify trusted caller-specific normalization at the digestion
  boundary.

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

Implementation status:

- implemented in `pyunitwizard`:
  - `to_nanometers`
  - `to_picoseconds`
  - `to_kelvin`
- added internal target-unit cache and reset hygiene

Practical note from implementation:

- these functions are useful as ecosystem helpers exactly because they are
  small, explicit, and boring;
- they should remain narrow and should not grow into a second generic
  conversion API.

### 2.3 Layer 3: SMonitor - Aggregated Observability
Instead of per-event signals, we use aggregated diagnostics to minimize instrumentation overhead:
- **Redundancy Monitor**: A stateful counter within SMonitor that tracks cumulative redundant conversions by callsite.
- **Audit Reports**: Provides developers with a "Top-N" list of performance leaks for manual refactoring post-1.0.

This layer should be treated as part of the ecosystem design space, not as a
fixed external constraint. If a better aggregated monitor requires changes in
SMonitor, those changes are in scope.

Implementation status:

- implemented in `smonitor` as an aggregated redundant-conversion counter in the
  manager report;
- connected in `pyunitwizard.convert()` fast paths to record redundant
  pass-through conversions by callsite;
- no per-event diagnostic flood was introduced.

Practical note from implementation:

- aggregation through the manager was the right design;
- a new event type per redundant conversion would have been much noisier and
  less useful.

## 3. First-Wave Implementation Snapshot

The first implementation wave has already produced concrete changes in all four
libraries.

- **PyUnitWizard**
  - canonical fast-tracks added;
  - redundant conversion callsite recording added.
- **ArgDigest**
  - `ValidatedPayload` added;
  - canonical science pipelines added.
- **MolSysMT**
  - caller-specific canonical array normalization introduced in private
    digesters for the first PBC chain (`box_lengths`, `box`);
  - selected `pbc` functions now accept either canonical arrays or quantities
    without changing their public API.
- **SMonitor**
  - aggregated redundant conversion counters exposed in manager reports.

This is enough to evaluate the architecture as real engineering work rather than
as a speculative roadmap.

## 4. Implementation Roadmap

1.  **Phase 1 (ArgDigest)**: Define the `ValidatedPayload` contract and the two-level pipeline logic.
    Status: done.
2.  **Phase 2 (ArgDigest)**: Implement semantic canonical pipelines such as `sci:nm_float64_payload`, `sci:ps_float64_payload`, and `sci:kelvin_float64_payload`, plus the final extractor step for kernel-facing naked arrays.
    Status: done.
3.  **Phase 3 (PyUnitWizard)**: Implement the first set of specialized fast-tracks (`to_nanometers`, `to_picoseconds`, `to_kelvin`).
    Status: done.
4.  **Phase 4 (MolSysMT)**: Update critical function decorators to leverage the new semantic payloads and kernel extractors, ensuring recursive calls do not repeatedly re-enter full PyUnitWizard digestion.
    Status: partially done.
    Current interpretation: the policy belongs primarily in caller-aware private digesters and, for hot structure routes, in local kernel-input helpers rather than in public API functions.
    Current scope:
    - initial PBC-oriented chain implemented;
    - coordinates-related structure routes implemented through
      `molsysmt.lib.structure._kernel_inputs`;
    - broader `time` and `temperature` routes still pending.
5.  **Phase 5 (SMonitor)**: Integrate the aggregated redundancy monitor for final auditing.
    Status: first version done.

Remaining near-term work:

- extend the MolSysMT side beyond the initial PBC chain into higher-value
  routes such as coordinates, time, and temperature;
- use the new diagnostics to confirm where redundant conversions still remain in
  realistic workflows;
- decide whether additional payload-bearing paths are worth adding, or whether
  caller-specific naked-array normalization is enough for most hot paths.

## 5. Second-Wave Refinement: Kernel Input Preparation

The next implementation step changed an important design conclusion from the
first wave.

The original experimental direction inside MolSysMT had started to move some
coordinates preparation into private digestion logic and, briefly, into
canonicalization helpers that forced coordinates into nanometers before
reaching `msmlib` kernels. That direction was rejected after a closer audit.

What the audit confirmed is:

- `molsysmt.lib.structure` kernels operate on numeric arrays and do not encode
  nanometer-specific semantics;
- public `structure` functions intentionally recover the numeric value, carry
  the working unit as `length_unit`, and then rebuild the public quantity using
  that unit;
- forcing `nm` in internal callers would therefore mix "kernel work unit" with
  "public output unit policy" and could add unnecessary conversions before and
  after the kernel.

The accepted refinement is narrower:

- PyUnitWizard now exposes a more explicit extraction service through
  `get_value()` and `get_value_and_unit()` by accepting `value_type` and
  `dtype`;
- MolSysMT keeps its kernel-specific preparation helpers locally in
  `molsysmt.lib.structure`, because those helpers do more than extraction:
  they also normalize coordinate shape for the Numba kernels and align units
  between paired inputs where needed.

This means the two libraries now split responsibilities more cleanly:

- **PyUnitWizard** provides the reusable extraction capability:
  value, unit, target container, and dtype;
- **MolSysMT** keeps the domain-specific policy for structure kernels:
  rank normalization, pairwise alignment, and kernel-facing input contracts.

Implementation status:

- implemented in `pyunitwizard`:
  - `get_value(..., value_type=..., dtype=...)`
  - `get_value_and_unit(..., value_type=..., dtype=...)`
- implemented in `molsysmt`:
  - `molsysmt.lib.structure._kernel_inputs.extract_coordinates_value_and_unit`
  - `molsysmt.lib.structure._kernel_inputs.align_coordinates_values_and_unit`
- adopted in MolSysMT for:
  - `get_center`
  - `get_distances`
  - `get_rmsd`
  - `get_least_rmsd`
  - `least_rmsd_fit`
  - `get_angles`
  - `get_dihedral_angles`
  - `principal_component_analysis`
  - `set_dihedral_angles`

Why this was worth doing:

- it reduces repeated boilerplate around `puw.get_value_and_unit(...)` and
  `np.asarray(..., dtype=np.float64)` in hot structure paths;
- it preserves the user-facing unit/output policy already present in MolSysMT;
- it advances the ecosystem goal of reducing gratuitous interaction with
  PyUnitWizard in internal kernels without weakening public semantics.

What remains open:

- evaluate whether `basic.get()` should eventually expose a dedicated internal
  path for structural consumers, or whether the new extraction options plus
  MolSysMT kernel helpers are already sufficient;
- extend the same thinking to other high-value routes such as `time` and
  `temperature` if profiling justifies it.

Initial measurement result:

- MolSysMT now ships a lightweight coordinate-path baseline in
  `../molsysmt/benchmarks/structure_coordinate_paths.py`;
- the first stable run uses the bundled `particles 4` `XYZ` trajectory to
  avoid conflating structure-path cost with heavier topology rebuilds;
- on that baseline, the local helper layer is clearly not the dominant cost:
  extraction/alignment stays below `1e-3 s` per call, while the full public
  wrappers (`get_center`, `get_distances`, `get_rmsd`) stay around
  `2.1e-1` to `2.6e-1 s`.

This is an important confirmation for the ecosystem plan:

- keeping domain-specific kernel preparation inside MolSysMT is not a
  measurable architectural mistake;
- if additional optimization is required, it is more likely to come from the
  public retrieval/wrapper path or from broader orchestration choices than from
  `_kernel_inputs` itself.

## 6. Validation Strategy

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

Validation snapshot from the first implementation wave:

- `pyunitwizard`: fast-track + diagnostics blocks green.
- `argdigest`: payload and science-pipeline tests green.
- `molsysmt`: private scientific-array digesters and initial PBC chain green.
- `smonitor`: redundant conversion aggregation tests green.

## 7. Expected Results

- **Stability**: Preserve the correctness and robustness already regained in PyUnitWizard, including the Astropy fixes.
- **Performance**: Substantially reduced overhead for repeated internal MolSysMT calls.
- **Maintainability**: Clearer boundaries; unit logic stays in the "digestion layer," while business logic stays in the "kernel layer."
- **Observability**: Better diagnostic visibility of redundant work without per-call event noise.

These are expected outcomes, not guarantees. They must be validated with both
microbenchmarks and real host-library scenarios.

## 8. Open Design Constraints

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

Additional constraint learned during implementation:

- in MolSysMT, argument-specific and caller-specific normalization rules are
  often a better insertion point than modifying public API functions directly.

## 9. Feedback Requested From The Other Team

Before broadening adoption, the most useful feedback would be:

- whether the current first-wave interpretation in MolSysMT looks correct,
  especially the choice to center the policy in private digesters;
- whether the next priority should be `coordinates`, `time`, `temperature`, or
  some other route with more practical impact;
- whether they expect more value from pushing `ValidatedPayload` deeper into
  internal call chains, or from expanding caller-specific canonical array
  normalization instead;
- whether the current aggregated redundancy reporting in SMonitor is sufficient
  for workflow diagnosis, or whether they need additional views or summaries.

## 10. Closure Criteria For This Document

This strategy document is temporary by design. It exists to carry the
cross-repository plan while the architecture is still being actively validated.

It can be retired once:

- the implementation phases recorded here are either completed or clearly
  downgraded to future work;
- the first-wave and second-wave conclusions have been incorporated into the
  stable devguide documents of `pyunitwizard`, `argdigest`, `molsysmt`, and
  `smonitor`;
- the other team has reviewed the implemented results and the follow-up
  adjustments have been made;
- the remaining work is tracked in normal roadmap/checklist documents instead
  of needing a dedicated strategy memo.

When that happens, the durable conclusions should be redistributed to the
relevant permanent documents and this file can be deleted.

---
*This plan represents the current consensus between the development team and the
ecosystem maintainers for the post-hardening performance and robustness work.
It should now be used to collect feedback on the first implementation wave
before broadening adoption further.*
