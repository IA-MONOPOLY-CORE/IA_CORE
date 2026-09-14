# Roadmap 4.x Macro-Mission 04

## P1 family coherence adjudication

## Decision

`ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_COMPLETE_SUBFAMILY_SPLIT_CONTRACTED`

The historical family label `P1_STATUS_OBSERVABILITY_MEMORY` remains part of
the Roadmap 3.x and 4.x lineage. It is not rewritten and its four routes are
not omitted from the 36-route inventory. The current evidence does establish
different future remediation boundaries, however, so one undifferentiated P1
implementation would have a larger blast radius and would mix unrelated
authority and data rules.

This is a documentary sequencing decision. No subfamily is remediated,
activated, exposed, or moved to Macro-Mission 05.

## Evidence used

The current handlers in `api.py`, local consumers in `ui/web`, the historical
36-route adjudication, the Roadmap 3.1 security audit, and the P1 source/payload
matrix were reviewed. The route matrix classifies every observation and does
not turn missing deployment, identity, tenant, retention, or external-consumer
evidence into a fact.

## Adjudicated subfamilies

### P1-A: platform status and health

Route: `GET /api/status`

The handler joins process-global supervisor state, provider diagnostics,
agent/tool inventories, hybrid-router state, loteria cycle state, runtime
counters, and a memory summary. It has known local UI consumers for overview,
hybrid, and connection polling. Its principal boundary is platform/operator
diagnostics, with a future need to separate minimal health from detailed
diagnostics. It is not currently a public health contract.

Future authority is therefore split between a bounded
`platform_status.read_minimal` and an Owner-authorized
`platform_status.read_detailed`. The full query must not bypass the latter.

### P1-B: protected memory reads

Route: `GET /api/memory`

The handler enumerates keys, reads history and orchestration details, and can
return a selected memory value. The repository does not establish whether
those values are global, user, tenant, or execution scoped, nor does it prove
ownership, redaction, retention, or no-enumeration behavior. It therefore
needs a content and ownership contract separate from platform status.

Future authority is Owner/operator for bounded metadata and audit projections,
and tenant-scoped only for explicitly sanitized, owned content. Raw memory is
never a compatibility promise.

### P1-C: protected logs and session events

Route: `GET /api/logs`

The handler reads a local log file, returns its path and raw tail, filters
warning/error strings, and returns process-global session events. The source
does not prove a log owner, retention, redaction, control-character policy,
tenant partition, or secret exclusion. Log sink, content classification, and
retention are distinct from memory ownership and must be tested separately.

Future authority is Owner/operator for a sanitized view. Raw diagnostics are
internal-only and never exposed to a tenant or external consumer.

### P1-D: domain dynamic metrics

Route: `GET /api/metrics/dynamic`

The handler reads loteria/evolution state, computes forward-test values, reads
V19 status, and returns a timestamp and phase. No current UI caller was found
in the source audit. Its future boundary is metric ownership and aggregation,
not the provider inventory or raw memory/log stores.

Future authority may be tenant business scope for proven aggregates or
Owner/operator for controlled operational detail. The current global response
is not a tenant contract.

## Coherence comparison

| Dimension | Status/health | Memory | Logs/events | Dynamic metrics |
| --- | --- | --- | --- | --- |
| Primary source | Supervisor, providers, hybrid router, runtime state | Memory manager and orchestration state | Filesystem log plus session events | Loteria/evolution state |
| Known local consumer | Overview, hybrid, connection polling | Admin memory panel | Admin logs panel | No current UI caller demonstrated |
| Candidate audience | Authenticated global or Owner/operator | Owner/operator; sanitized tenant projection | Owner/operator; internal raw diagnostics | Tenant business or Owner/operator |
| Core missing proof | Identity, detailed-view policy, deployment | Ownership, tenant scope, retention, redaction | Sink owner, retention, redaction, tenant split | Owner, aggregation, audience, correlation risk |
| Primary risk | Platform/provider reconnaissance | Raw content and key enumeration | Raw log/secret/PII disclosure | Cross-tenant activity inference |
| Compatibility shape | Minimal versus detailed split | Sanitized projection | Sanitized event/log view | Versioned aggregate contract |
| Remediation owner | Platform status/observability | Memory/observability | Observability/logging | Domain metrics/observability |

These differences are contractual and operational, not merely naming. They
prove that the four routes should not be repaired as one shared payload or one
shared capability.

## First future subfamily selection

Only one subfamily is selected for a later, separately authorized mission:

`P1-A_PLATFORM_STATUS_HEALTH_SELECTED_NOT_STARTED`

The selection is reproducible using the authorized criteria:

| Criterion | Status/health | Memory | Logs/events | Dynamic metrics |
| --- | ---: | ---: | ---: | ---: |
| Risk reduction | 5 | 5 | 5 | 3 |
| Centrality | 5 | 4 | 4 | 2 |
| Internal readiness | 4 | 3 | 2 | 3 |
| Low external dependency | 4 | 3 | 3 | 4 |
| Low blast radius | 4 | 2 | 2 | 4 |
| Reversibility | 5 | 4 | 4 | 5 |
| Evidence quality | 5 | 2 | 2 | 2 |
| **Total** | **32** | **23** | **22** | **23** |

Status/health wins because it is the most central known local read surface, its
source chain is directly characterized, and a bounded minimal-versus-detailed
contract is reversible without deciding memory ownership or metric tenancy.
The score does not authorize a code change or public health endpoint.

## Non-selected routes

Memory, logs/events, and dynamic metrics remain in the P1 family with their
own future contracts and are `DEFERRED_NOT_STARTED`. No order, priority, or
scope beyond the selected status/health entry is implied. The historical
destinations remain preserved as historical lineage, while active future
exposure remains `DEFAULT_DENIED`.

## No hard frontier

There is no `TRUE_HARD_FRONTIER_P1_FAMILY_BOUNDARY`: the evidence supplies a
clear boundary and the authorized criteria select the first subfamily without
requiring an unresolved Direction choice. If a later design attempts to
combine these subfamilies into one capability, it must stop and reopen this
adjudication.

## Guardrails

- `P1_STATUS_OBSERVABILITY_MEMORY` remains the historical family name.
- `P1-A_PLATFORM_STATUS_HEALTH` is selected but not started.
- No other P1 subfamily is selected for implementation.
- No route is exposed externally.
- No route receives a new capability in production.
- No payload v2, endpoint, adapter, runtime, execution, provider, store,
  memory product, UI, or integration is created.
- Macro-Mission 05 is not started.
