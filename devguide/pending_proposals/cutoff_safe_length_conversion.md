---
summary: Define single-rounding length extraction for inclusive cutoffs.
issue: uibcdf/pyunitwizard#143
status: open
opened: 2026-11-09
closed:
verification: measured
area: [core, interoperability]
guard:
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
and excludes the same distance. A backend switch therefore provides an
example-specific result with ordinary backend rounding.

## Proposed operation

Add an explicit mode to fixed-unit extraction, for example
`get_value(quantity, to_unit=target, rounding="single")`. The name is a
proposal for review under #143. Read the original magnitude and source unit
before any rescaling, and return the correctly rounded binary64 magnitude in
the explicit target unit, using round to nearest with ties to even.

- Start with finite scalar binary64 values and homogeneous float64 arrays.
  Accept integer scalars that are exactly representable in binary64 so
  quantities such as `500 pm` can use the same path. Preserve array shape
  and the input quantity. Require an explicit target and use its unit
  identity independently of session standards.
- Start with the exact multiplicative length definitions nm, angstrom and
  pm. Accept aliases and native units only when the adapter can establish
  the corresponding definition. A matching display name or approximate
  registry match alone leaves the definition unverified. Report unsupported
  units, registries and backends explicitly. Begin with the Pint route used
  by #666 and qualify additional adapters against the same oracle before
  claiming them.
- For these three units the ratio is an exactly representable integer or its
  reciprocal. One binary64 multiply by that integer, or one divide by it,
  suffices. The reference prototype matches 405/405 array entries drawn from
  the 27 cases under five source backends and three standards. Its arithmetic
  used the declared ratios directly. Adapter identity checks still need
  implementation and qualification. A separate range probe produced 51/51
  finite matches and detected all three overflowing cases.
- Define overflow as an explicit error. Use binary64 rounding for subnormals
  and zero, including signed zero. Reject nonfinite input and combinations
  that ask for policy standardization or a different output dtype in this
  mode. Offset units and general compound scales require separate contracts.

## Comparison limits and consumer boundary

The guarantee concerns the destination float. For example, the predecessor
of the binary64 value `1.6` and `1.6` angstrom both round to `160.0` pm,
although the former's exact converted value is below 160 pm. A requirement
to preserve that physical inequality would call for exact comparison or an
explicit downward-rounded cutoff against distances already in the target
binary64 unit. Those are distinct contracts from the requested nearest-rounded
magnitude. Coordinate conversion, geometry and periodic box arithmetic also
have their own rounding.

MolSysMT's `digest_threshold` currently calls `standardize` after validating
length. `get_contacts` then extracts the cutoff in nm for validation and in
the calculation unit for comparisons. Preserve the original threshold
magnitude and unit through digestion and apply the agreed extraction once in
the calculation unit. MolSysMT owns that boundary and the native geometry,
including dense, cell-list and periodic behavior. [Consumer issue](https://github.com/uibcdf/molsysmt/issues/666)

## Acceptance criteria

- Agree the public mode and supported unit/backend identities with MolSysMT.
- Check all 27 destination bit patterns for scalars and homogeneous arrays
  with explicit targets under each non-default policy. Cover unsupported
  definitions, finite range extremes, signed zero and source/policy integrity.
- Receive the operation at the native MolSysMT cutoff boundary, with the
  original predecessor, equality and successor controls in dense and
  cell-list routes, including periodic cases. Keep the inclusive predicate.
