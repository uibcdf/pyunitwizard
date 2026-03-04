# Integrating Your Library

For existing codebases, the safest migration strategy is progressive. Start at
public boundaries and move inward only when behavior is stable.

The first step is central configuration. Define one initialization path where
supported backends, parser, form, and standard units are set explicitly.

Then update API entry points so inbound quantities are normalized before domain
logic runs. In practice, this means converting to a canonical form and using
`check(...)` or `are_compatible(...)` to enforce dimensional contracts.

Once inbound data is controlled, standardize outputs on public return paths.
This prevents hidden unit drift between modules and reduces integration bugs in
downstream tools.

Finally, harden the migration with tests:
- success and failure paths for conversion and validation,
- regression tests for previously observed unit bugs,
- fixture-level reset/reconfiguration to avoid shared mutable state.

A migration is usually ready for production when unit assumptions are explicit,
behavior is reproducible across environments, and failures are actionable for
users.

If your roadmap includes multiple backends, use
[Backend Coverage and Expectations](backend-coverage.md) before expanding
support claims.

For common failures and quick diagnosis, continue with
[Troubleshooting](troubleshooting.md).
