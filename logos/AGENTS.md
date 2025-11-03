# Logos

Always follow the repository-wide guidelines in the root `AGENTS.md` together with the rules below.

## Scope
These instructions apply to every asset inside `logos/`, including raster and vector files as well as supporting metadata.

## Purpose
This directory stores the canonical PyUnitWizard branding assets consumed by the documentation build and any future distribution channels. Treat the files here as the single source of truth for the project logo.

## Editing Guidance
- Keep the logo design consistent with the current PyUnitWizard branding: reuse the existing color palette, proportions, and typography unless a refresh has been agreed with maintainers.
- Update the master artwork (`logo.svg` / `logo_paths.svg`) first; derive other formats from that source to avoid divergence.
- Export raster assets at multiple resolutions only when specifically requested. Name additional exports clearly (e.g., `logo@2x.png`) and document them in `logos/README.md`.
- Preserve vector files as plain SVGs saved with Inkscape compatibility. Strip editor metadata only if it does not remove reusable layer information.
- Do not compress or minify assets in ways that hinder future editing. Keep original layers, groups, and text paths intact.

## Coordination
- When changing the logo, notify maintainers so dependent documentation, marketing material, and themes can be updated together.
- If the logo is used by the Sphinx theme, confirm the path in `docs/conf.py` and `_static/` assets still points to the correct file after modifications.

## Review Checklist
1. Verify that `logo.svg` renders correctly in browsers and in the Sphinx HTML build (`make html`).
2. Ensure derived files (`logo.png`, `logo_paths.svg`, etc.) are regenerated from the latest master artwork.
3. Update `logos/README.md` with the rationale for the change, export settings, and any new asset locations.
4. Remove temporary working files before committing; only commit finalized assets.
