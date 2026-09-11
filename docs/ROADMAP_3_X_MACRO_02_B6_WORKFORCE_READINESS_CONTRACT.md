# Roadmap 3.x Macro-Mission 02: B6 Workforce Readiness Contract

`ROADMAP_3X_MACRO_02_B6_WORKFORCE_READINESS_CONTRACT_MATERIALIZED`

## Conditional entry

B4-A/B and B5-A/B provide the internal postconditions required for a
contract-only workforce readiness map: permission/activation boundaries are
fail-closed, persistence families have ownership classifications, and sandbox
rollback is bounded and idempotent. B4-B still requires external provider and
credential evidence.

## Readiness map

| Surface | Repository contract | Current state |
| --- | --- | --- |
| lineage | `core/agent_lineage_schema.py` | contract available |
| profile | catalog/profile schemas and materializers | contract and sandbox inputs available |
| role/specialization | catalog registries and profile contracts | declarative source available |
| preset | `core/agent_preset_materializer.py` and preset contracts | sandbox/declarative only |
| paper | `core/agent_paper_schema.py`, paper seed materializer | schema/sandbox only |
| agent | agent permission and active contract schemas | no active workforce |
| team | `core/sandbox_team_schema.py`, materializer, read model | sandbox/declarative only |
| model recommendation | provider/model metadata and hardware profile | recommendation only; provider evidence pending |
| approval | `core/approval_workflow.py`, confirmation gate, active contract | explicit approval contract; no approval granted |
| activation state | `core/runtime_activation_gate.py`, `core/operational_readiness_gate.py` | blocked/pre-runtime contract |
| runtime gate | runtime and lifecycle contracts | runtime/execution disabled |
| persistence owner | B5-A matrix and audit persistence schema | GOKV/sandbox strongest; legacy ownership unresolved |
| rollback | B5-B sandbox integral rollback | sandbox rollback proven; product rollback not claimed |

## Classification

`CONTRACT_READY_INTERNAL_NO_ACTIVE_WORKFORCE`

This is a readiness classification for future controlled preparation. It does
not mean an agent, team, provider, model session, permission, memory namespace,
or business workforce is active. No live workforce is created, registered,
started, or connected.

## Explicit blockers

- External identity, deployment, tenant, provider reachability, credential
  presence, egress, and cost evidence remain pending.
- Legacy route coverage remains `UNKNOWN` for all 36 routes.
- Product persistence ownership and operational rollback remain unresolved for
  legacy surfaces.
- Any future activation still requires the permission, confirmation, readiness,
  approval, and rollback chain in order.

## Boundary

No agents, teams, providers, integrations, endpoints, payloads, runtime,
execution, memory stores, product data, or network traffic were created or
used. This station only records static contract readiness and its blockers.
