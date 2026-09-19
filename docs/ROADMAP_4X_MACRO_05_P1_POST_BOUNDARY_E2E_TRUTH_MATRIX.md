# Roadmap 4.x Macro-Mission 05 - P1 Post-Boundary E2E Truth Matrix

## Mission identity

```text
ROADMAP: 4.x
MACRO_MISSION: 05
MISSION_NAME: P1_POST_BOUNDARY_E2E_ADVERSARIAL_ASSURANCE_AND_INTERNAL_FAMILY_CLOSURE
BASELINE: 9148f023f4df8e642f396f08a6386f8967d70efb
BRANCH: main
EXTERNAL_EXPOSURE: DEFAULT_DENIED
P1_STARTING_STATE: FUNCTIONALLY_COMPLETE_PENDING_E2E_CLOSURE
```

This is the live Macro 05 matrix. Historical Macro 03 matrices remain
unchanged and retain their original deferred claims.

```text
P1_FAMILY_STATE: INTERNALLY_CLOSED
P4_ROUTES_INTERNALLY_CLOSED: 7
P1_ROUTES_TREATED_AFTER_CLOSURE: 4
ROUTES_TREATED_TOTAL: 11
ROUTES_REMAINING: 25
MACRO_06_RECALIBRATION_AND_NEXT_FAMILY_SELECTION: SELECTED_NOT_STARTED
```

## Canonical request flow

```text
HTTP request
-> bounded selector parsing
-> server-side resolver
-> canonical principal validation
-> exact capability gate
-> scope/tenant gate
-> sensitive source read
-> allowlist projection and sanitization
-> versioned schema validation
-> bounded JSON response
```

Every denied request must stop before the sensitive source read. No route may
derive authority from a client-controlled header, cookie, query value, Origin,
Host, User-Agent, Forwarded value, loopback address or body.

## Four-route live matrix

| Route | Contract | Views | Capability | Identity | Source | Deny-before-source | Success shape | Consumer | Tenant | External |
|---|---|---|---|---|---|---|---|---|---|---|
| `GET /api/status` | `platform_status.v1` | `minimal`, `full=true` detailed | minimal is local; detailed `platform_status.read_detailed` | server resolver for detailed | local supervisor lifecycle for minimal; bounded local snapshot for detailed | yes for detailed | exact status allowlist | Overview uses minimal; Hybrid uses `full=true` | not applicable | default denied |
| `GET /api/memory` | `protected_memory.v1` | `metadata`, `audit`; `tenant` future/inactive | `memory.metadata.read`, `memory.audit.read_sanitized`; tenant future `memory.tenant.read_sanitized` | server resolver | supervisor memory only after gate | yes | exact metadata/audit allowlists | HUD Memory | tenant 404/no enumeration | default denied |
| `GET /api/logs` | `protected_logs.v1` | `summary`, `events` | `observability.logs.read_sanitized` | server resolver | bounded `api.log` and session events after gate | yes | exact summary/events allowlists | HUD Logs | tenant selector cannot establish scope | default denied |
| `GET /api/metrics/dynamic` | `protected_dynamic_metrics.v1` | `summary` only | `observability.metrics.read_sanitized`; tenant `tenant_metrics.read` future/inactive | server resolver | legacy dynamic snapshot projected to neutral aggregate after gate | yes | exact bounded neutral summary | no current UI consumer | tenant 404/no enumeration | default denied |

## Route inventory truth

The historical canonical matrix contains 36 stable routes. Current inspection
confirms the four P1 paths above and seven P4 routes already internally
closed. Macro 05 treated exactly four P1 GET routes and added no route, alias,
method or view. Eleven routes are now treated across the closed P4 and P1
families; 25 remain outside this mission.

## Preserved boundaries

P0, P2-P9, P4 behavior, HTML, CSS, i18n, Request Draft Panel, widgets,
providers, integrations, stores, runtime, execution, payload v2, secrets,
CORS, global auth, production tenancy, Cognitive Kernel, Enterprise Foundry,
Cyber Range, IA_CORE OS and Method Santi 3.2.3 remain outside product scope.

## Gaps intentionally remaining

There is no trusted production identity resolver, demonstrated tenant
ownership, tenant isolation, retention implementation or external consumer
evidence. These remain default-denied or future-only and are not closed by
this mission.
