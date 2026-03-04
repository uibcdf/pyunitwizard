# Serialization of Quantities

## Motivation

Scientific workflows frequently require storing quantities with units in files,
databases, or network APIs. Without a standardized serialization format,
unit information can be lost or misinterpreted.

Typical storage formats include:

- JSON
- YAML
- HDF5
- NetCDF
- Parquet

## Design Goal

PyUnitWizard should provide a **canonical serialization format** for quantities.

Example representation:

{
  "value": [1,2,3],
  "unit": "nm",
  "dimensionality": {"L":1}
}

## Proposed API

puw.serialize(quantity)
puw.deserialize(data)

## Benefits

- reproducible scientific workflows
- safe storage of units
- compatibility with data pipelines
