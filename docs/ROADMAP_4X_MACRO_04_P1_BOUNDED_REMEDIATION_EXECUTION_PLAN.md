# Roadmap 4.x Macro-Mission 04

## Bounded P1 remediation execution plan

## State

`PREPARED_NOT_STARTED`

This plan is a future execution contract. It does not authorize execution in
Macro-Mission 04, and it does not begin Macro-Mission 05. The current mission
has modified no product surface and has not added an endpoint, capability,
middleware, schema, adapter, runtime path, or payload.

Macro-Mission 04.1 establishes an architectural precedence checkpoint before
P1-A. Therefore P1-A remains
`P1-A_PLATFORM_STATUS_HEALTH_SELECTED_NOT_STARTED` and is
`TEMPORARILY_PAUSED_BEHIND_COGNITIVE_KERNEL_RECONCILIATION`. This pause does
not start remediation or change any route.

## Exact first unit

`P1-A_PLATFORM_STATUS_HEALTH_SELECTED_NOT_STARTED`

Included route:

- `GET /api/status`, only as a future bounded status/health read.

Excluded from this unit:

- `GET /api/memory`;
- `GET /api/logs`;
- `GET /api/metrics/dynamic`;
- all other legacy routes;
- P0, P4, widgets, Request Draft Panel, UI, payload v2, runtime, execution,
  providers, integrations, stores, secrets, and external exposure.

The selected unit must first decide whether a minimal health response can be
separated from the current detailed diagnostic response without breaking a
proven consumer. `full=true` is not an authorization mechanism and cannot
select a privileged view by itself.

## Candidate implementation boundary for a later mission

Only after a separately accepted execution mission may the following units be
considered:

- the `api.py:get_status` handler, limited to response selection and policy
  enforcement;
- a dedicated status access/policy helper, if the existing repository does
  not provide a suitable boundary;
- a dedicated status projection/sanitizer, if required to remove provider,
  model, path, tool, and activity detail.

The current mission creates none of these helpers and changes no production
logic. Provider diagnostic callables, memory stores, runtime startup, and
hybrid-router implementation are not remediation targets in this plan.

When P1-A eventually starts, its status projection must use a generic
`domain_module_status` representation with parity across modules. The legacy
domain-specific branch currently observed in the diagnostic surface is a
`legacy singled-out domain status` debt item, not a privileged feature. The
migration must be versioned, consumer-tested, sanitized and reversible.

## Proposed capabilities

The following names are inactive proposals only:

- `platform_status.read_minimal`;
- `platform_status.read_detailed`.

The minimal capability is sufficient only for the minimal platform view. The
detailed capability is sufficient only for an Owner-authorized operator view.
Neither capability grants write, runtime, execution, provider, integration,
secret, memory, log, metric, tenant, or root authority.

## Authorization order

A future resolver must evaluate in this order and deny on any missing or
ambiguous result:

1. verified identity source;
2. authentication for the intended audience;
3. canonical principal and role;
4. explicit capability;
5. deployment and trusted-origin policy where applicable;
6. global platform scope or explicitly assigned operator scope;
7. field classification and redaction result;
8. versioned consumer compatibility;
9. response serialization.

No step may infer permission from performance, empty strings, wildcards,
casing, query parameters, subscription tier, or inherited tenant data.

## Scope, projection and sanitization

The minimal view may contain only a deliberate liveness/readiness result. It
must not contain provider names, model names, health messages, filesystem
paths, tool or agent inventory, hybrid details, cycle limits, activity counts,
tenant identifiers, credentials, secrets, or timing that enables meaningful
reconnaissance.

The detailed view, if separately approved, remains Owner/operator-only and
must use an explicit allowlist. It must redact internal paths, secret-bearing
configuration, credentials, tokens, private prompts, tenant content, and
unbounded provider diagnostics. The projection must not copy raw memory, logs,
or metric payloads into status.

Status has no current pagination contract. A future minimal view should have
no collections. Any future detailed collection must have an explicit bound
and ordering contract before implementation; line-count, list size, or
`full=true` cannot replace authorization.

There is no new retention policy in this plan. Status responses are ephemeral
reads; any persisted audit record would require a separate ownership,
retention, redaction, and rollback decision.

## Error and compatibility contract

Future denial must be indistinguishable from an unavailable protected view
where revealing route existence or provider state would enable enumeration.
The exact error code and safe detail require contract tests before activation.
No error may echo secrets, raw paths, tenant identifiers, provider exceptions,
or unredacted configuration.

Known local consumers must be inventoried before changing the response:

- `ui/web/admin-panels.js` overview and hybrid loaders;
- `ui/web/index.html` connection polling.

No external consumer is assumed. A response change requires a versioned
compatibility decision, positive consumer tests, negative unknown-consumer
tests, and explicit evidence for any external audience. Compatibility cannot
preserve unsafe fields merely because they are currently returned.

## Required gates

The first unit remains inactive until all applicable gates are evidenced:

| Gate | Required evidence | Current state |
| --- | --- | --- |
| `G01_IDENTITY_SOURCE` | Stable identity and principal source | `INACTIVE_EVIDENCE_REQUIRED` |
| `G02_AUTHENTICATION` | Authentication for private beta audience | `INACTIVE_EVIDENCE_REQUIRED` |
| `G03_AUTHORIZATION` | Exact role/capability resolution and fail-closed denial | `INACTIVE_EVIDENCE_REQUIRED` |
| `G04_TENANT_ISOLATION` | Proof that global/operator view cannot cross tenant boundaries | `INACTIVE_EVIDENCE_REQUIRED` |
| `G05_CORS_TRUSTED_ORIGINS` | Explicit trusted origins if browser exposure changes | `INACTIVE_EVIDENCE_REQUIRED` |
| `G06_INGRESS_HOSTING` | Actual deployment and ingress boundary | `INACTIVE_EVIDENCE_REQUIRED` |
| `G18_EXTERNAL_CONSUMER_COMPATIBILITY` | Demonstrated consumers and version strategy | `INACTIVE_EVIDENCE_REQUIRED` |
| `G19_PAYLOAD_RESPONSE_CONTRACT` | Stable bounded response and negative contract tests | `INACTIVE_EVIDENCE_REQUIRED` |

External exposure remains `DEFAULT_DENIED`. No gate is activated by this plan.

## Tests required before any future activation

Positive tests must prove the minimal and, separately, authorized detailed
projection for a canonical principal. Negative tests must cover missing or
ambiguous identity, wrong role, absent capability, wildcard/empty/case-variant
capabilities, `full=true` bypass attempts, unauthorized origin, tenant
boundary ambiguity, provider exception leakage, path/secret leakage, and
unknown external consumers.

The later mission must also replay the focused status contract, relevant
historical guards, P4 protections, secret policy, JSON census, and protected
diff checks. If the response boundary changes browser or deployment behavior,
an E2E run is mandatory. This plan itself requires no route invocation.

## Rollback and stop conditions

Rollback must be a local, reviewable revert of the future status unit and must
restore the prior route behavior without touching unrelated P1 subfamilies.
Rollback ownership belongs to the future Owner-authorized platform/observability
owner; naming an owner here does not assign current permission.

Stop before implementation if any of the following remains unresolved:

- identity, audience, capability, or operator authority;
- tenant or global scope;
- safe minimal/detailed split;
- redaction or secret policy;
- consumer compatibility;
- deployment, origin, or hosting boundary;
- an exception that can leak internal data;
- a need to modify memory, logs, metrics, providers, runtime, execution, UI,
  payload, or another protected surface;
- any request to activate Macro-Mission 05.

## Future acceptance criteria

The selected unit can be considered complete only when the code diff is
limited to the approved status boundary, all gates have an evidence-backed
state, positive and negative tests pass, local consumers remain compatible,
external exposure is explicitly accepted or remains denied, and rollback is
demonstrated. A green test result alone is not permission to expose the route.

Until then, the only valid state is:

`P1-A_PLATFORM_STATUS_HEALTH_SELECTED_NOT_STARTED`
`PREPARED_NOT_STARTED`
`EXTERNAL_EXPOSURE_DEFAULT_DENIED`

## Current roadmap cursor after Macro 04.2

Macro 04.2 completed the inert Cognitive Kernel G0 adversarial assurance and
released this selected unit as the next roadmap cursor, without implementing or
invoking it:

`NEXT_SELECTED_NOT_STARTED`

The prior `TEMPORARILY_PAUSED_BEHIND_COGNITIVE_KERNEL_RECONCILIATION` state is
historical context from Macro 04.1. P1-A remains not started, all activation
gates remain inactive, and external exposure remains `DEFAULT_DENIED`.
