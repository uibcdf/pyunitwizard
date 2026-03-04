# Pandas Interoperability

## Motivation

Many scientific workflows rely on pandas DataFrames for data analysis.

However, pandas does not natively support quantities with units.
This often leads to:

- units being dropped
- quantities converted to object dtype
- inconsistent handling across workflows

## Design Goal

PyUnitWizard should provide utilities to safely integrate quantities
with pandas structures.

## Possible Interfaces

puw.Series(quantity)
puw.attach_units(df)

## Benefits

- safer data science workflows
- explicit unit handling in tabular data
- improved integration with analytics pipelines
