---
summary: Define single-rounding length extraction for inclusive cutoffs.
issue: uibcdf/pyunitwizard#143
status: resolved
opened: 2026-11-09
closed: 2026-11-11
verification: measured
area: [core, interoperability]
guard: tests/pint/test_length_rounding.py::test_pint_length_boundaries_round_once
normative:
blocked_by: []
supersedes: []
---

# Single-rounding length extraction

## What

MolSysMT compares a distance with an inclusive cutoff in the calculation
unit. Equivalent cutoffs of 0.5 nm, 5 angstrom and 500 pm should include the
reported 0.5 nm contact. Adjacent cutoff values provide separate negative
and positive controls. [MolSysMT #666](https://github.com/uibcdf/molsysmt/issues/666)

The requested provider contract is to scale the original binary64 magnitude
by an exact ratio and round once in the explicit target unit. The current
public API delegates arithmetic to the selected backend. `get_value` applies
`dtype` and `value_type` to the result of that arithmetic. `conversion_factor`
returns a float derived from backend conversions of zero and one. Record
extraction also uses backend arithmetic when converting to a different unit.
`are_equal` compares converted magnitudes and `are_close` applies a tolerance.

## Measured behavior

On Linux with Python 3.14.7, NumPy 2.4.6 and PyUnitWizard source `f82b618`, the
runtime tree matches tag 0.29.1. The consumer's 0.28.1 observation is separately
recorded in #666. In the source probe with Pint 0.25.3, `get_value` converts
5 angstrom and 500 pm to 0.49999999999999994 and 0.4999999999999999 nm.

The following counts compare `get_value(..., to_unit=...)` with the 27 pinned
vectors. Scalars and homogeneous float64 arrays give the same counts.

| Source backend | Bit matches | Inclusive decisions matching the reference |
| --- | ---: | ---: |
| Pint 0.25.3 | 19/27 | 23/27 |
| OpenMM 8.6.1 | 26/27 | 27/27 |
| unyt 3.1.0 | 22/27 | 25/27 |
| Astropy 8.0.1 | 15/27 | 23/27 |
| OpenFF Units 0.4.0 | 19/27 | 23/27 |

Multiplying by `conversion_factor` produces the same counts in each measured
backend. Pint-backed `QuantityRecord.to_quantity(unit=...)` produces 19/27
bit matches and 23/27 decisions. The reference file was read from commit
`758ba2963bffcda24677132c03df28ca88f4001d`, SHA-256
`4a3a31521ab3e160474279e9eb07357c0ddd2bcbc405904fa5559dd687d90aac`.
The rational computation independently reproduced all 27 expected bits and
decisions. [Pinned reference](https://github.com/uibcdf/molsysmt/blob/758ba2963bffcda24677132c03df28ca88f4001d/devtools/data/unit_scale_boundary_reference_666_20261110.json)

An explicit OpenMM route reproduces the decisions in the measured example.

```python
import numpy as np
import pyunitwizard as puw

values = np.array([np.nextafter(5.0, -np.inf), 5.0, np.nextafter(5.0, np.inf)])
cutoff = puw.quantity(values, "angstrom", form="pint", parser="pint")
nm = puw.convert(cutoff, to_unit="nm", to_form="openmm.unit", to_type="value", parser="pint")
assert (0.5 <= nm).tolist() == [False, True, True]
```

Explicit conversion through OpenMM also reproduced 81/81 decisions and
78/81 bit patterns per source backend across nm, angstrom and pm session
standards. In each policy the predecessor of 5 angstrom converts to
`0x1.fffffffffffffp-2` nm while the rational reference is
`0x1.ffffffffffffep-2`. The distinction at 0.5 nm survives that difference.
At another boundary, 7 angstrom converts through OpenMM to
`0.7000000000000001` nm. That includes a distance at the successor of
`0.7` nm, while the requested single-rounding conversion returns `0.7` nm
and excludes the same distance.

OpenMM groups powers of ten before materializing the floating-point factor.
For angstrom and pm to nm it obtains `0.1` and `0.001`, respectively. Pint
0.25.3 multiplies the source scale by the reciprocal of the target scale
using binary64 intermediates and obtains `0.09999999999999999` and
`0.0009999999999999998`. Multiplying those smaller factors by 5 and 500
explains the original discrepancy. [OpenMM conversion source](https://github.com/openmm/openmm/blob/8.6.1/wrappers/python/openmm/unit/unit.py) and [Pint conversion source](https://github.com/hgrecco/pint/blob/0.25.3/pint/facets/plain/registry.py)

A separate probe derived all nine ratios from Pint 0.25.3's standard unit
definitions using `UnitRegistry(non_int_type=Fraction)`. Multiplying binary64
magnitudes by the ratios cast to float matched 26/27 reference bits. Using
one multiply or divide by the exact integer matched 27/27, as did scaling
the exact rational magnitudes and rounding once at the end.

## Proposed conversion behavior

The initial sketch exposed `rounding="single"` on `get_value`. The review
favors improving ordinary unit conversion for scales whose exact definitions
PyUnitWizard can establish. Callers already specify the destination through
`get_value(quantity, to_unit=target)` or `convert(quantity, to_unit=target)`.
Centralize the rule in their shared conversion path so that every caller of a
qualified pair receives the same rounding. Start with the verified Pint
length definitions needed by #666. Qualify each additional adapter before
including it in that guarantee.

Read the original magnitude and source unit before rescaling. For supported
inputs, return the correctly rounded binary64 magnitude in the destination
unit, using round to nearest with ties to even. Select the ordinary backend
conversion when the exact path does not apply.

- Start with finite scalar binary64 values and homogeneous float64 arrays.
  Accept integer scalars that are exactly representable in binary64 so
  quantities such as `500 pm` can use the same path. Preserve array shape
  and the input quantity. Require an explicit target and use its unit
  identity independently of session standards.
- Start with the exact multiplicative length definitions nm, angstrom and
  pm. Establish eligibility from trusted unit definitions before a registry
  translation can erase their origin. An approximate registry match or a
  matching display name supplies insufficient evidence for this path.
  Validate aliases and unit objects against their actual definitions.
- For these three units the ratio is an exactly representable integer or its
  reciprocal. One binary64 multiply by that integer, or one divide by it,
  suffices. The reference prototype matches 405/405 array entries drawn from
  the 27 cases under five source backends and three standards. Its arithmetic
  used the declared ratios directly. Adapter identity checks still need
  implementation and qualification. A separate range probe produced 51/51
  finite matches and detected all three overflowing cases.
- Qualify range behavior, including overflow, subnormals and signed zero.
  Review result dtype and backend return types against the existing API
  contract before selecting eligible inputs. Offset units, arbitrary registry
  definitions and general compound scales remain outside the new guarantee.
  Check the effect on exact-output consumers such as record creation and
  reference vectors before changing conversion dispatch.

## Comparison limits and consumer boundary

The guarantee concerns the destination float. For example, the predecessor
of the binary64 value `1.6` and `1.6` angstrom both round to `160.0` pm,
although the former's exact converted value is below 160 pm. A requirement
to preserve that physical inequality would call for exact comparison or an
explicit downward-rounded cutoff against distances already in the target
binary64 unit. If that contract is needed, place it at the common comparison
boundary. A route that compares squared distances must define the cutoff in
that representation as well. The nearest-rounded length conversion is the
smaller provider change for the reported cases. Coordinate conversion,
geometry and periodic box arithmetic also have their own rounding.

MolSysMT's `digest_threshold` currently calls `standardize` after validating
length. `get_contacts` then extracts the cutoff in nm for validation and in
the calculation unit for comparisons. Preserve the original threshold
magnitude and unit through digestion and apply the agreed extraction once in
the calculation unit. MolSysMT owns that boundary and the native geometry,
including dense, cell-list and periodic behavior. [Consumer issue](https://github.com/uibcdf/molsysmt/issues/666)

## Acceptance criteria

- Agree the corrected ordinary conversion contract and supported unit/backend
  identities with MolSysMT. Verify that the usual explicit-target call
  receives the corrected conversion without an additional option.
- Check all 27 destination bit patterns for scalars and homogeneous arrays
  with explicit targets under each non-default policy. Cover unsupported
  definitions, finite range extremes, signed zero and source/policy integrity.
- Receive the operation at the native MolSysMT cutoff boundary, with the
  original predecessor, equality and successor controls in dense and
  cell-list routes, including periodic cases. Keep the inclusive predicate.

## Source implementation and checks — 2026-11-10

The existing `convert` and `get_value` calls now select single-rounding
arithmetic for the verified nm, angstrom and pm definitions in PyUnitWizard's
Pint registry. The adapter compares the current definitions with the standard
definitions it checked at registry creation. A multiplication or division
by an exact integer implements the conversion for binary64 values, float64
arrays and exactly representable integer scalars. Pint contexts and other
definitions use the native operation. The dispatcher checks source registry
identity before normalization, including the conversion nested in record
creation. This preserves the established handling of foreign quantities.

The public regression failed before the change. It now matches each of the
27 reference values for scalar and array input under each of the three
length policies. It tests result bits, inclusive decisions and input/policy
integrity. The additional cases cover aliases, integer and string inputs,
float64 range edges, float32 behavior, approximate foreign registry matches
and active Pint context overrides. A direct check against the pinned
MolSysMT JSON produced 81/81 bit matches and decisions across the three
standards. The minimum Pint 0.25 run passed all 36 selected tests.

The complete serial run on Python 3.14.7, NumPy 2.4.6 and Pint 0.25.3 passed
1,050 cases. JUnit records eight skips, including five at optional module
collection. The run used temporary Physipy and Quantities installations
and an offline wheelhouse for the installed-consumer build. A parallel
attempt exposed two existing parser-state-dependent cases, reproduced
against the pre-change source with unyt loaded first. The normal serial
order passes those cases. The Sphinx HTML build and applicable Ruff checks
pass.

A downstream source smoke used the live MolSysMT checkout and its available
native extension with the modified PyUnitWizard source. Public
`get_contacts` returned the expected decision for all 108 combinations of
the 27 vectors, dense or cell-list selection and vacuum or orthogonal
periodic geometry. The periodic pair crossed a box face. The source result
can be received and qualified by the MolSysMT owner under #666. In general,
preserving the original cutoff until the computation boundary also prevents
additional rounding when the calculation unit differs from the session
standard. [MolSysMT #666](https://github.com/uibcdf/molsysmt/issues/666)

The conversion shipped in 0.29.2. Each of the 30 installed profiles executed
all 27 boundary cases. A clean public installation also passed the cutoff
suite. MolSysMT owns independent consumer receiving under #666.
[Publication record](release_0.29.2.md)
