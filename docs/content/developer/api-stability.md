# API Stability

PyUnitWizard is on the pre-1.0 stabilization path.

## Stability rules

- Do not break documented public symbols without migration notes.
- Keep behavioral contracts deterministic across supported Python versions.
- Treat the completed `0.18.x` through `0.21.x` lines as historical contract
  baselines.
- Keep `0.22.x`/`0.23.x` hardening additive and backward compatible unless a
  documented correctness fix requires otherwise.

## Contract references

- `devguide/roadmap.md`
- `devguide/minimum_quantity_protocol_contract.md`
- `devguide/frontend_transparent_mode_contract.md`
- `devguide/release_1.0.0_checklist.md`
