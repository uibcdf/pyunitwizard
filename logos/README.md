# PyUnitWizard Logo Assets

This directory stores the official PyUnitWizard logo files used by the
documentation build and any downstream publications. Treat these assets as the
single source of truth for the project branding.

## Files
- `logo.svg` – master vector artwork with editable layers and guides.
- `logo_paths.svg` – flattened vector version with text converted to paths for
  compatibility in environments without the project fonts.
- `logo.png` – raster export used by the Sphinx theme (`docs/_static/logo.png`).

Additional exports (sizes, backgrounds, formats) should be derived from
`logo.svg` and documented here when introduced.

## Editing Workflow
1. Open `logo.svg` in Inkscape (or another SVG editor) with Varela Round
   installed to preserve typography. Keep the color palette and proportions
   consistent with the current design unless a rebrand has been approved by the
   maintainers.
2. Apply changes in the master file, keeping layers and guides intact for
   future edits. Save as plain SVG to maintain Inkscape compatibility metadata.
3. Regenerate the derived files:
   - Use **File → Save As** to produce `logo_paths.svg` with text converted to paths.
   - Export `logo.png` at 512×512 (or the resolution requested by the docs
     team) using transparent background and no compression artifacts.
4. Preview the assets:
   - Open `logo.svg` and `logo_paths.svg` in a browser to ensure they render without missing fonts.
   - Copy `logo_paths.svg` to `docs/_static/logo.svg` and replace the existing `logo.png`.
   - Run `make html` inside `docs/` to confirm the Sphinx build picks up the refreshed logo.
5. Update this README whenever you change the artwork, export settings, or introduce new derivative assets.

## Usage Notes
- The documentation theme expects the raster logo at `docs/_static/logo.svg` (a copy of `logo_paths.svg`).
- Other projects should reference the vector version (`logo.svg`) whenever possible to avoid quality loss.
- Do not commit intermediate working files, previews, or exported formats that
  are not referenced by the documentation or approved distribution channels.

For automation and review requirements, see `logos/AGENTS.md`.
