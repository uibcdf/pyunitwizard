# Sandbox

Always follow the guidelines in the root `AGENTS.md` in addition to the notes below.

## Scope
These instructions apply to all files inside `sandbox/` and any subdirectories created for ad-hoc experiments.

## Purpose
`sandbox/` is a scratch space for quick experiments, manual tests, and
throwaway notebooks. Nothing here ships with the library or its documentation
builds.

## Guidance
- Keep experiments self-contained and clearly labeled; remove stale files once they are no longer useful.
- Avoid adding new dependencies—use only what is already available in the development environment.
- Do not rely on sandbox code for automated tests, documentation examples, or package features.
- Store large datasets or generated artifacts outside the repository; only
  commit lightweight assets needed to explain an experiment.

## Review Checklist
1. Confirm that no changes in `sandbox/` are required for releases, tests, or docs.
2. Ensure any notebooks run without side effects and do not require external credentials.
3. Delete or archive obsolete scratch files before requesting review.
