# Performance Baseline

This directory stores lightweight baseline scripts for release-candidate
performance checks.

Current baseline script:

- `conversion_baseline.py`: measures median/min/max time per call for hot
  API paths (`convert`, `get_form`, `is_quantity`, string parsing).

Run:

```bash
python devtools/benchmarks/conversion_baseline.py
```

The RC process stores snapshots under `devguide/` so regressions can be
compared between candidate tags.
