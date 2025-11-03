# Physical constants in PyUnitWizard

The `pyunitwizard.constants` module exposes a small catalog of dimensioned physical constants that can be retrieved through
`get_constant()` or listed with `show_constants()`. Each entry is stored as a magnitude/unit pair so the value can be converted
through PyUnitWizard's quantity abstraction.

## Canonical constants

| Canonical name    | Value (SI)                | Description |
|-------------------|---------------------------|-------------|
| `Avogadro`        | `6.02214076e+23 1/mole`   | Avogadro's number. |
| `Universal gas`   | `8.13446261815324 J/(kelvin*mole)` | Universal (molar) gas constant. |
| `Boltzmann`       | `1.380649e-23 J/kelvin`   | Boltzmann constant. |

Use the canonical names when calling `get_constant()` to avoid ambiguity. The function returns a PyUnitWizard quantity, which can be
converted into another unit by supplying the `to_unit` argument, or transformed into a different library form (e.g., Pint, Unyt) via
the `to_form` argument.

## Synonym mapping

The module also supports several shorthand names. Synonyms resolve to the canonical names shown above before the constant is
looked up.

| Synonym | Canonical name |
|---------|----------------|
| `NA`    | `Avogadro` |
| `R`     | `Universal gas` |
| `Molar gas` | `Universal gas` |
| `KB`    | `Boltzmann` |

When you add new synonyms, make sure the canonical name already exists in `_constants` and that `show_constants()` lists all
related aliases together.

## Adding or updating constants

Follow these steps whenever you introduce a new constant or adjust an existing one:

1. Update the `_constants` dictionary with the canonical name and its magnitude/unit pair.
2. Add or adjust entries in `_constants_synonyms` so any new shorthands resolve to the canonical name.
3. Confirm the `quantity()` helper is still used to construct the runtime quantity and that conversions continue to flow through `convert()`.
4. Document the new constant (including synonyms and default unit) in this README so users know it is available.
5. Add regression tests that cover direct lookup, synonym lookup, and at least one conversion into an alternate unit or form.
6. Run `pytest` (or a more targeted subset) to ensure the new entries work across supported backends.

By keeping the dictionaries synchronized and verifying conversions, you preserve compatibility across all libraries supported by PyUnitWizard.
