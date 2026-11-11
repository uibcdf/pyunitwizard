---
summary: Reuse resolved Pint unit definitions for string-unit construction.
issue: uibcdf/pyunitwizard#142
status: partial
opened: 2026-11-08
closed:
verification: measured
area: [construction, conversion, performance]
guard: tests/test_conversion_branches.py::test_pint_string_unit_builds_only_the_requested_quantities
normative:
blocked_by: []
supersedes: []
---

# Pint string-unit construction

OpenCASTp wraps its physical results in quantities through the public
`quantity(value, unit_string)` API. Unit resolution is already cached.
The conversion path used to construct a magnitude-one quantity from the
resolved unit and immediately extract that unit before building the requested
quantity. [OpenCASTp performance work](https://github.com/uibcdf/opencastp/issues/13)

The shortcut applies when both parser and output form are Pint and no target
unit was supplied. It copies the native unit wrapper around the resolved
definition, so callers still receive separate unit objects. The existing
policy resolution and diagnostic decorators remain in the call path. Explicit
target conversions and translation through other parsers keep their existing
dispatch.

The regression observes the Pint quantity factory after unit resolution has
warmed. Two public construction calls originally built four quantities,
including two of magnitude one. The candidate builds exactly the two requested
quantities and preserves their float bits, units and object independence.

Four fresh Python 3.14 processes with Pint 0.25.3 used the order
baseline/candidate/candidate/baseline, one logical CPU and single-threaded
numerical libraries. The PyUnitWizard baseline was `6417e3a`. Both source
snapshots ran without cached project bytecode. Eight warmed batches per
variant each called the public quantity factory 4,566 times using the values
and three angstrom powers in #142. Every result had the expected float bits
and unit, and all 4,566 objects in each batch were distinct.

The same processes ran the public `opencastp.analyze()` using the
`rough_surface_carbon` and `onion_shells_3_carbon` inputs from the performance
manifest at OpenCASTp `3a8f2508a5bfd78263fccab4b69582e779ede49b`. There was one
warmup per input and process, followed by two timed analyses. Fingerprints
computed outside the timed calls covered all result fields, including the
feature magnitudes and units, mesh arrays, and execution metadata. All eight
fingerprints per input agreed.

| Workload | Baseline wall / CPU median (ms) | Candidate wall / CPU median (ms) |
| --- | ---: | ---: |
| 4,566 string-unit constructions | 109.652 / 109.646 | 89.469 / 89.428 |
| 75-atom rough surface | 344.411 / 344.266 | 348.030 / 347.945 |
| 517-atom onion shells | 2103.836 / 2103.179 | 2021.002 / 2020.406 |

The construction reduction was 18.4%. Whole-analysis samples overlapped for
both inputs. The small input's median wall time increased by 1.1% and the
larger input's decreased by 3.9%. These timings describe two synthetic
inputs on the selected Python engine. The original large molecular analysis
and current native engine remain for OpenCASTp receiving after publication.

The joint source run with #141, #143 and #144 passes 1,055 tests on Python
3.14 with twelve workers. JUnit records eight skips, including five optional
module collections. The Pint 0.25 run passes all 71 selected conversion,
registry and guide-bootstrap tests. Ruff, the report index and Sphinx HTML
checks pass.
