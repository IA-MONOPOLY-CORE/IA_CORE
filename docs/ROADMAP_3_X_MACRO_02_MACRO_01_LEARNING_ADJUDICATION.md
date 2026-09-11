# Roadmap 3.x Macro-Mission 02: Macro 01 Learning Adjudication

`ROADMAP_3X_MACRO_02_MACRO_01_LEARNING_ADJUDICATION_MATERIALIZED`

## Decision

Macro-Mission 01 produced six reusable observations. They were recovered from the route reconnaissance, B-3 coverage, checkpoint, and existing boundary documents. Each was compared with the current GOKV vocabulary before storage.

All six are stored as `CANDIDATE`, not `VALIDATED` or `PROMOTED`:

| Knowledge ID | Generality | Current state | Reason not promoted |
| --- | --- | --- | --- |
| `derive_service_owner_before_destination` | reusable for route-boundary work | CANDIDATE | one development-origin mission; no independent confirmation |
| `callable_chain_is_not_authorized_route` | reusable for provider and activation audits | CANDIDATE | source-callability evidence is not field authorization evidence |
| `legacy_write_needs_boundary_proof` | reusable for persistence and materialization audits | CANDIDATE | no operational write or rollback exercise was performed |
| `partial_security_fix_does_not_assign_owner` | reusable for partial remediation review | CANDIDATE | one partial security fix does not establish the remaining owner |
| `read_only_method_is_not_read_authz` | reusable for exposed read surfaces | CANDIDATE | identity, ownership, and exposure evidence remain external/unknown |
| `contract_exists_is_not_route_adapter` | reusable for canonical coverage audits | CANDIDATE | no route adapter was implemented or proven |

No duplicate was forced into the vault. No existing item was rewritten. No item was promoted automatically. The event, metric, and post-block loop are append-only and point to the four Macro 01 commits.

## OCI consequence

The six candidates remain excluded from `PROMOTED_ONLY` and ordinary inherited packs. They can be inspected during an explicit `DEVELOPMENT_VALIDATED` mission only if a future request and compatibility filters select them after their lifecycle state is advanced by a separately evidenced decision. This station does not advance lifecycle state.

## Boundary

This is GOKV metadata, evidence, schema validation, and documentation only. It does not alter API routes, permissions, payloads, runtime, execution, providers, integrations, product data, or external traffic.
