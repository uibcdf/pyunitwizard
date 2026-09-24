# Serialization Contract Draft (Post-1.0 Candidate)

Status: **superseded** (2026-09-24) by `QuantityRecord`, the inert interchange form
(`pyunitwizard/record.py`; issue uibcdf/pyunitwizard#82; design record #83; report
`pending_proposals/quantity_record.md`). Kept as history. Its safety rules are all met
by the new design: versioned format (`qrec/0.3`), dimensional validation on read, explicit
errors for missing or malformed fields, and no implicit backend import. Its promotion
gate is met by two real integration cases: uibcdf/sabueso#32 and uibcdf/molsysmt#240. The
`form` field of the payload below was dropped: a record is independent of the backend it
came from.

## Goal

Define a canonical schema for exchanging quantities safely in data pipelines,
APIs, and persisted artifacts.

## Proposed canonical payload

```json
{
  "value": [1.0, 2.0, 3.0],
  "unit": "nanometer",
  "form": "pint",
  "dimensionality": {"[L]": 1}
}
```

## Field semantics

1. `value` (required)
- scalar or array-like numerical payload.

2. `unit` (required)
- canonical string unit representation.

3. `form` (required)
- source backend form identifier (`pint`, `openmm.unit`, etc.).

4. `dimensionality` (optional in transport, recommended in validation)
- canonical dimensionality map for integrity checks.

## Safety rules

1. Explicit schema versioning is required before this becomes stable API.
2. Deserialization must validate dimensional compatibility when target unit is
   requested.
3. Missing or malformed mandatory fields must raise explicit errors.
4. No implicit backend imports should occur without configured support.

## Promotion gate to active roadmap

Promote this draft only when:
- two real integration use cases require it,
- testable schema-validation behavior is defined,
- migration semantics for future schema evolution are documented.
