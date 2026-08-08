# Proposal: Unit-Configuration Authority Across MolSysSuite

## Status

Pending architectural decision and cross-repository validation.

## Motivation

MolSysSuite libraries such as MolSysMT, MolSysViewer, TopoMT, and
PharmacophoreMT configure default quantity forms, parsers, and standard units
through PyUnitWizard. This is convenient when each library is used alone, but
all imported libraries share the same PyUnitWizard kernel inside one Python
process. A script or Jupyter kernel that uses several suite libraries therefore
needs an explicit answer to three questions:

1. Who owns the session-wide unit policy?
2. Which settings may a library change without affecting its siblings?
3. How can library-specific output contracts coexist with a user-selected
   session policy?

The answer must not depend on import order, lazy-import order, notebook cell
execution order, or which library happens to create an object last.

## Confirmed Current Situation

PyUnitWizard stores the following values in a process-global kernel:

- the default output form;
- the default string parser;
- standard units and their derived dimensional maps and matrices;
- standardization and conversion caches;
- loaded backends and parsers;
- dynamically registered fast-track conversions.

Several MolSysSuite libraries currently execute calls equivalent to
`set_default_form()`, `set_default_parser()`, and `set_standard_units()` from
their `_pyunitwizard.py` modules. The configured profiles are not identical:

- MolSysMT and TopoMT use nanometers, picoseconds, kelvin, daltons,
  elementary charge, kilojoules per mole, and radians;
- MolSysViewer is nearly equivalent but currently spells the mass unit as
  `amu`;
- PharmacophoreMT includes both kilocalories and kilojoules per mole and uses
  degrees.

Because these calls update one shared kernel, the last configuration applied
wins. With lazy imports, "last" may mean the last library whose unit bridge was
first accessed, not necessarily the last top-level package imported. In a
notebook, module caching and out-of-order cell execution make this even harder
to reason about.

Explicit conversion to a requested unit remains well-defined, but operations
that rely on `standardize()`, the default quantity form, the default parser, or
derived standard-unit lookup can change behavior after an unrelated sibling
library is activated.

## Additional Risk in the Current Context Manager

`pyunitwizard.context()` is useful but does not yet constitute a safe solution
for library coexistence:

- it mutates the same process-global kernel;
- overlapping thread or asynchronous contexts are not isolated;
- concurrent readers can observe temporary or partially rebuilt state;
- restoration currently covers the main standard dictionaries but not every
  derived matrix, derived-unit list, or cache rebuilt by
  `set_standard_units()`;
- fast-track registrations and backend state are outside its snapshot.

The restoration completeness must be tested and corrected before contexts are
recommended as the general isolation boundary.

## Recommended Authority Rule

Unit policy should follow this precedence, from strongest to weakest:

1. an explicit target unit, form, or parser supplied to an API call;
2. an explicitly activated local context or immutable unit-policy object;
3. configuration selected by the application or interactive session;
4. PyUnitWizard factory defaults.

Importing a library must not outrank any of these levels. In particular, a
library must not silently replace process-wide defaults merely because it was
imported or lazily activated.

### Preferred MolSysSuite simplification

Because MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT, and the other sibling
tools are one coordinated family, the preferred first solution is a single
shared PyUnitWizard policy for the whole working session. PyUnitWizard should
define or explicitly activate that policy once; sibling libraries should only
consume it. Importing or first using another MolSysSuite library must not
reconfigure the session.

Under this model, the user or application may change the PyUnitWizard session
defaults once and every sibling observes the same result. Library-specific
profiles are not required for the initial solution. They remain a possible
future extension for genuinely different ecosystems or isolated workflows.

The implementation decision still needs to determine whether the shared
MolSysSuite policy is PyUnitWizard's factory default or an explicit built-in
profile activated at session startup. The lowest-friction option for the
coordinated suite is a coherent factory default, provided PyUnitWizard's wider
general-purpose audience accepts that domain-oriented choice.

The application is the natural owner of session policy. In a standalone
script, the application is the script. In Jupyter, it is the notebook kernel
configuration chosen by the user. A high-level MolSysSuite launcher may provide
a shared convenience profile, but that profile must be explicitly selected and
must not become an implicit dependency of the individual libraries.

## Separate Three Different Concepts

The implementation and documentation should distinguish:

### Quantity representation

The default backend or form used to return quantities, such as Pint or
OpenMM. This is a representation preference and may reasonably be selected by
the user for a session.

### String parsing

The backend used to parse textual quantities. It is an input concern and does
not by itself define scientific output units.

### Scientific standard units

The canonical units used when an operation requests standardization without an
explicit target. These affect observable API results and scientific
serialization, so they require stronger stability and provenance than a
display preference.

Treating all three as one undifferentiated global configuration makes both API
contracts and debugging harder.

## Proposed Architecture

### 1. Stop unconditional library-owned global configuration

MolSysSuite libraries should not call process-wide setters unconditionally at
import time. Their `_pyunitwizard.py` modules may:

- ensure required backends are available;
- register a named library profile;
- register non-conflicting optimized conversions;
- expose internal helpers;
- validate compatibility with the active policy.

They should not activate their profile globally unless the user or application
explicitly requests it. Under the preferred shared-policy solution, sibling
libraries do not need to register profiles at all; they simply consume the
active PyUnitWizard session policy.

### 2. Build and replace the session policy atomically

Evaluate an internal or public immutable object such as `UnitPolicy` or
`Configuration`, containing at
least:

- default form;
- default parser;
- canonical units indexed by dimensionality;
- a stable profile name and optional version;
- provenance describing who selected it;
- derived lookup data built atomically from the declared units.

An immutable, fully built policy can be swapped atomically and avoids readers
seeing `set_standard_units()` halfway through reconstruction. It can also be
stored with serialized scientific data when reproducibility requires it.

### 3. Treat named profiles as an optional extension

Named profiles are not necessary when the whole MolSysSuite uses one shared
session policy. If future non-suite consumers or specialized workflows require
them, candidate APIs to evaluate include:

```python
puw.configure.register_profile("molsysmt", policy)
puw.configure.register_profile("pharmacophoremt", policy)
puw.configure.set_session_profile("molsyssuite-si")

with puw.context(profile="molsysmt"):
    result = operation()
```

Registration must be idempotent. Re-registering the same name with different
content must raise a diagnostic rather than silently replacing it.

Profiles are declarations, not ownership claims. Importing MolSysMT may make a
`molsysmt` profile available, but it must not automatically activate it.

### 4. Decide the local-isolation mechanism explicitly

Two implementation levels should be evaluated with prototypes and concurrency
tests:

- `contextvars`-based policy resolution, which supports nested, thread, and
  asynchronous task-local contexts when all policy reads go through an
  accessor;
- serialized process-global contexts, which are simpler but block overlapping
  writers and still allow unrelated readers to observe temporary values.

For PyUnitWizard's long-term multipurpose role, context-local policy resolution
is preferable if the accessor migration is practical. If 1.0 retains a
process-global context, the limitation must be explicit and its writer
serialization and complete restoration must be tested. It must not be called
thread-safe when it only serializes writers.

### 5. Make library contracts independent of ambient defaults

An operation whose scientific contract requires nanometers, picoseconds,
radians, or kilojoules per mole should request that unit explicitly at its API
boundary. Ambient standardization should be reserved for APIs whose documented
purpose is to follow the active user policy.

Each MolSysSuite API should classify its outputs as one of:

- canonical scientific output with a fixed documented unit;
- policy-following output using the active unit policy;
- backend-preserving output;
- unitless numerical output after an explicit conversion boundary.

This classification prevents a visualization preference from changing a
molecular-mechanics result.

### 6. Govern fast-track registrations

Fast-track names are also process-global. Registration should be idempotent and
conflict-aware, and either use canonical unit semantics or namespaced aliases.
A sibling package must not silently redefine a fast track registered by
another package.

### 7. Preserve user authority in interactive sessions

For notebooks, provide one documented setup cell and an introspection report:

```python
puw.configure.set_session_profile("molsyssuite-si")
puw.configure.report()
```

The report should state the active form, parser, standard units, profile,
provenance, and any registered sibling profiles. Re-importing or first using a
library later in the notebook must not change the report.

## Suite-Wide Default Policy

A common MolSysSuite policy is the preferred baseline for suite documentation,
interactive work, and integration tests. It should reconcile at least:

- `dalton` versus `amu` spelling;
- radians versus degrees;
- whether energy-per-mole has exactly one canonical standard;
- whether visualization-only dimensions such as milliseconds belong in the
  scientific profile;
- fixed scientific output contracts versus user-selectable display units.

The shared policy does not prevent explicit domain conversions. For example, a
pharmacophore display may request degrees while core geometry continues to
calculate and serialize angles under its documented contract.

## Required Evidence

Before choosing and implementing the architecture, build a cross-repository
evidence matrix covering MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT, and at
least one combined application.

### Import and activation permutations

Test every relevant ordering of imports and first unit-aware calls. After each
step, record the active policy and verify that unrelated activation does not
change prior-library output contracts.

### Script and notebook lifecycles

Test:

- a fresh Python process;
- repeated imports;
- notebook-style out-of-order activation;
- reset and reconfiguration;
- serialization followed by loading under a different active profile.

### Concurrency

Test nested contexts, overlapping threads, asynchronous tasks, exceptions, and
readers outside a context. Verify that restoration includes every derived
matrix, unit list, and cache.

### Scientific outputs

At minimum compare coordinates, time, angles, energy, force, mass, charge,
viewer geometry, and pharmacophore descriptors. Test both explicit-unit APIs
and policy-following APIs.

### Diagnostics

Require structured diagnostics for:

- conflicting profile registration;
- implicit attempts to replace an application-selected policy;
- incomplete or dimensionally ambiguous profiles;
- unsupported forms or parsers;
- non-isolated contexts when concurrency is attempted.

## Migration Plan

1. Inventory all import-time configuration and all calls that depend on
   ambient standardization across MolSysSuite.
2. Add import-order permutation tests that reproduce current conflicts.
3. Fix complete state snapshot and restoration in `pyunitwizard.context()`.
4. Decide and document whether 1.0 contexts are context-local or serialized
   process-global state.
5. Introduce atomic immutable session-policy replacement behind a small
   experimental API.
6. Define and ratify the shared MolSysSuite default policy; defer named profiles
   unless evidence shows they are necessary.
7. Migrate library scientific invariants to explicit target units.
8. Remove unconditional library activation so sibling libraries consume the
   shared session policy; add profile registration only if later evidence
   justifies it.
9. Add a compatibility period with diagnostics for legacy import-time
   configuration.
10. Publish script and Jupyter guidance and run the cross-repository matrix in
    CI.

## Acceptance Criteria

The proposal is complete when:

- importing or lazily activating any combination of MolSysSuite libraries does
  not silently change the active unit policy;
- import order and notebook cell order do not alter documented scientific
  results;
- the authority precedence is part of the public contract;
- contexts restore all derived state and have a tested concurrency contract;
- every stable library API declares whether its outputs are fixed-unit,
  policy-following, backend-preserving, or unitless;
- any enabled profile mechanism and all fast-track conflicts produce
  deterministic diagnostics;
- the active policy and its provenance are introspectable;
- combined MolSysSuite tests exercise the behavior in Python 3.11, 3.12, and
  3.13.

## Recommendation

Treat this as a pre-1.0 interoperability decision for PyUnitWizard, even if the
full context-local architecture is delivered incrementally. At minimum, 1.0
should prevent silent import-order ownership, repair context restoration, state
the concurrency limitation honestly, and define the authority precedence.

The central principle is simple: PyUnitWizard owns the mechanism and the shared
session default, the application or user may override that session policy, and
each sibling library owns only its documented API contracts.
