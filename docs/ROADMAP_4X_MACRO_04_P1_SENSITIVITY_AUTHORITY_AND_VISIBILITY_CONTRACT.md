# Roadmap 4.x Macro-Mission 04

## P1 sensitivity, authority and visibility contract

## Status

`ENTRY_REVIEW_COMPLETE_REMEDIATION_NOT_STARTED`

This is a future contract for the four legacy read routes. It records the
minimum security and visibility boundary that a later mission must prove. It
does not change `api.py`, add authentication, add authorization, change CORS,
rewrite payloads, or expose any route.

Current route behavior and future required behavior are intentionally separate.
The current repository has no route-level identity or P1 authorization
dependency for these handlers. Therefore the current exposure disposition is:

`EXTERNAL_EXPOSURE_DEFAULT_DENIED`

The beta is private. No anonymous route is authorized by this document.

## Visibility categories

| Category | Meaning in a future contract | P1 use |
| --- | --- | --- |
| `PUBLIC_HEALTH_MINIMAL` | Only a deliberately minimal liveness/readiness fact, with no topology, provider, model, path, tenant, or activity detail. | A possible future health successor only; no current P1 route qualifies. |
| `AUTHENTICATED_GLOBAL` | An authenticated, explicitly global principal may read a bounded platform view. | Minimal global status only after identity, audience, and deployment evidence. |
| `TENANT_BUSINESS` | A tenant principal may read data for its own tenant and authorized business scope. | Tenant-scoped metrics or sanitized business observability only after scope proof. |
| `OWNER_OR_OPERATOR_ONLY` | The Owner or a specifically authorized operator may read sensitive operational views. | Detailed status, sanitized memory, and sanitized logs. |
| `INTERNAL_SYSTEM_ONLY` | Internal service diagnostics are not a user or tenant surface. | Raw diagnostics and source-level details. |
| `NEVER_EXPOSE` | Data must not leave its protected store or controlled redaction boundary. | Secrets, raw memory, raw logs, credentials, private prompts, and unredacted tenant content. |
| `UNKNOWN_DEFAULT_DENY` | The repository does not prove safe visibility. Deny until evidence and policy exist. | Current default for unclassified P1 fields and scopes. |

## Constitutional authority

Santi remains final authority. The Owner or an explicitly delegated policy may
approve a future capability, but a successful request, a high performance
score, an empty identity, a wildcard, or a case variant never creates global
authority. A read capability is not a write capability, and visibility is not
permission to alter runtime, execution, providers, or integrations.

Every future resolver must fail closed when identity, role, audience, tenant,
capability, or scope is absent or ambiguous. It must use canonical typed
principals and exact capability values. It must not derive authority from
strings, wildcard matching, casing normalization, or inherited tenant data.

## Route contracts

### `GET /api/status`

The current response combines supervisor running state, provider names and
diagnostics, agent and tool inventories, hybrid-router information, loteria
cycle state, runtime counters, and a memory summary. The current handler has
no route-level authentication or authorization dependency. This makes the
route a detailed diagnostic surface, not public health.

Field disposition for a future successor:

| Data | Current evidence | Future category | Future authority |
| --- | --- | --- | --- |
| Minimal liveness boolean | Field exists as `running`, but its safe audience is not established. | `PUBLIC_HEALTH_MINIMAL` only for a newly bounded health view, not this response. | `AUTHENTICATED_GLOBAL` by default; anonymous only with explicit external evidence. |
| Provider names, health messages and model names | Returned in `providers`. | `OWNER_OR_OPERATOR_ONLY` or `INTERNAL_SYSTEM_ONLY`. | `platform_status.read_detailed`, proposed and inactive. |
| Agent and tool inventories | Returned in `agents` and `overview.tools`. | `OWNER_OR_OPERATOR_ONLY`. | `platform_status.read_detailed`, proposed and inactive. |
| Hybrid snapshot and safe-mode details | Returned when the router/configuration supplies it. | `OWNER_OR_OPERATOR_ONLY`; exact redaction remains unknown. | `platform_status.read_detailed`, proposed and inactive. |
| Cycle and loteria limits | Returned when the domain is available. | `TENANT_BUSINESS` only if the owner and tenant mapping are proven; otherwise `UNKNOWN_DEFAULT_DENY`. | `tenant_observability.read`, proposed and inactive. |
| Runtime counters and memory path/count summary | Returned in `overview`. | `INTERNAL_SYSTEM_ONLY` for paths; bounded `OWNER_OR_OPERATOR_ONLY` for counters. | Separate capabilities, never a broad global read. |

The existing route must remain default-denied for external exposure until a
future mission proves identity, audience, deployment, compatibility, and a
minimal/detailed split. A `full` query parameter must never bypass policy.

### `GET /api/memory`

The current route enumerates memory keys, reads history, loads an orchestration
detail, and returns a selected key value when `key` is supplied. The route does
not establish whether the memory is global, user, tenant, or execution scoped;
it does not establish ownership, retention, redaction, or cross-tenant rules.

| Data | Current evidence | Future category | Future authority |
| --- | --- | --- | --- |
| Key names and counts | Returned by the memory manager and summary. | `OWNER_OR_OPERATOR_ONLY`; `UNKNOWN_DEFAULT_DENY` until enumeration policy exists. | `memory.metadata.read`, proposed and inactive. |
| History and latest execution detail | Returned from memory and supervisor state. | `OWNER_OR_OPERATOR_ONLY` after ownership and retention proof. | `memory.audit.read_sanitized`, proposed and inactive. |
| Selected value | Returned without route-level content sanitization. | `NEVER_EXPOSE` in raw form; only an explicitly sanitized view may become `TENANT_BUSINESS`. | `memory.tenant.read_sanitized`, exact tenant scope required, proposed and inactive. |
| Memory path | Returned in status. | `INTERNAL_SYSTEM_ONLY` and omitted from user payloads. | No user capability. |

No future memory read may accept an unscoped global key lookup on behalf of a
tenant. The principal, tenant, business scope, record ownership, retention
class, and redaction result must be resolved before content selection. Missing
or ambiguous ownership must produce a fail-closed response without revealing
whether another tenant's key exists.

### `GET /api/logs`

The current route tails `config.LOG_DIR / api.log`, returns the path and raw
lines, filters warnings and errors by substring, and appends the last 50
in-memory session events. The current source does not prove an admin identity,
sink ownership, retention, redaction, control-character handling, or tenant
partitioning.

| Data | Current evidence | Future category | Future authority |
| --- | --- | --- | --- |
| Filesystem path | Returned as `path`. | `INTERNAL_SYSTEM_ONLY`; never a tenant field. | No user capability. |
| Raw log lines | Returned by `_tail_log`. | `NEVER_EXPOSE` until sanitized and policy-bound. | No raw-log capability. |
| Sanitized warnings/errors | Current values are only substring filters, not a proven sanitizer. | `OWNER_OR_OPERATOR_ONLY` after a redaction contract. | `observability.logs.read_sanitized`, proposed and inactive. |
| Session events | Returned from process-global state. | `OWNER_OR_OPERATOR_ONLY` after event classification and retention proof. | `observability.events.read_sanitized`, proposed and inactive. |

Future log views must remove or redact secrets, tokens, headers, credentials,
PII, customer data, private business data, sensitive prompts, raw payloads,
stack traces, internal paths, and control characters. The user-visible view
must be bounded by severity, tenant, time, retention, and page/cursor policy.
No line-count parameter may substitute for authorization or redaction.

### `GET /api/metrics/dynamic`

The current route reads loteria/evolution statistics, calculates forward-test
values, reads V19 status, adds a timestamp, and returns the current phase. No
tenant or metric owner is resolved by the route, and no current UI caller was
demonstrated in the source audit.

| Data | Current evidence | Future category | Future authority |
| --- | --- | --- | --- |
| Aggregate domain metrics | Returned under `forward_test`. | `TENANT_BUSINESS` only after aggregation and tenant ownership proof; otherwise `UNKNOWN_DEFAULT_DENY`. | `tenant_metrics.read`, proposed and inactive. |
| Phase and V19 state | Returned in `fase_actual` and `v19`. | `OWNER_OR_OPERATOR_ONLY` or a tenant-safe derived view after policy proof. | `observability.metrics.read_sanitized`, proposed and inactive. |
| Timestamp | Generated in the response. | `TENANT_BUSINESS` only when correlation risk is assessed. | Same bounded metric capability. |

No metric response may reveal another tenant's activity, provider usage,
strategy, cost, infrastructure, or identifiable execution timeline through
aggregation, cardinality, timestamp correlation, or error behavior.

## Capability and role minimums

These are proposals for a later design, not active permissions:

| Future role | Necessary capability | Sufficient scope | Explicitly excluded |
| --- | --- | --- | --- |
| Anonymous/public | None for current P1 routes. | No P1 data. | Detailed status, memory, logs, metrics. |
| Authenticated global operator | `platform_status.read_minimal` | Global minimal status only. | Provider/model inventory, raw memory, raw logs, tenant data. |
| Owner-authorized operator | `platform_status.read_detailed`, `memory.metadata.read`, `memory.audit.read_sanitized`, `observability.logs.read_sanitized`, `observability.events.read_sanitized` | Only the operational scope explicitly assigned by the Owner and policy. | Raw secrets, unredacted memory, arbitrary tenant enumeration. |
| Tenant business reader | `tenant_metrics.read` or `memory.tenant.read_sanitized` | One resolved tenant and authorized business scope, with row/content redaction. | Other tenants, global memory, platform internals, credentials. |
| Internal service | Internal service capability defined in a separate system contract. | Only the minimum diagnostic store and retention class. | User-facing authority, inherited tenant secrets, global root. |

Capability names are case-sensitive canonical identifiers. Empty strings,
wildcards, missing principals, or inherited capabilities are not valid grants.
No role receives a broad `admin.read_all` convenience capability.

## Current versus future decision

| Dimension | Current repository | Future requirement |
| --- | --- | --- |
| Authentication | Not demonstrated at these route signatures. | Verified identity source and audience binding. |
| Authorization | Not demonstrated for P1. | Exact capability and role resolution, fail closed. |
| Tenant isolation | Not demonstrated for P1. | Explicit tenant principal, ownership, and no-enumeration tests. |
| CORS/deployment | Localhost default, wildcard rejected, credentials disabled. | Hosting and trusted-origin evidence before any external exposure. |
| Retention | Not established for memory/logs. | Owner, duration, deletion, backup, and audit policy. |
| Redaction | Not established for memory/logs. | Field/content-classification and adversarial redaction tests. |
| Compatibility | Local UI callers exist for status/memory/logs; external callers unknown. | Consumer inventory and versioned response strategy. |

Until every applicable future requirement is evidenced, each affected route
remains `REMAIN_DISABLED_OR_CONTAINED` and
`EXTERNAL_EXPOSURE_DEFAULT_DENIED`.
