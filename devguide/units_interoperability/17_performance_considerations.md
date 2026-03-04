# Performance Considerations

## Motivation

Interoperability layers can introduce overhead if not carefully designed.

PyUnitWizard should remain lightweight and avoid unnecessary computational costs.

## Key Strategies

Lazy conversions
Avoid converting units unless necessary.

Zero-copy extraction
Extract numerical values without duplicating memory where possible.

Dimensional caching
Cache dimensional representations to avoid repeated computation.

## Goals

- minimal overhead compared to native unit libraries
- predictable performance in numerical pipelines
