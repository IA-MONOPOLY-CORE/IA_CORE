# Roadmap 4.x Macro-Mission 04

## Bounded P1 remediation execution plan

## State

`P1-A_PLATFORM_STATUS_HEALTH_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`

Macro-Mission 04.3 executed the bounded P1-A unit on the real repository. The
only product route changed was `GET /api/status`; its minimal view is a cheap,
provider-neutral local lifecycle projection and its `full=true` compatibility
alias is a separately capability-gated detailed projection. No new route,
provider, runtime, execution, tenant, payload or external exposure was added.
Macro-Mission 05 remains not started.

## Exact first unit

`P1-A_PLATFORM_STATUS_HEALTH_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`

Included route:

- `GET /api/status`, as the bounded status/health read completed by P1-A.

Excluded from this unit:

- `GET /api/memory`;
- `GET /api/logs`;
- `GET /api/metrics/dynamic`;
- all other legacy routes;
- P0, P4, widgets, Request Draft Panel, payload v2, runtime, execution,
  providers, integrations, stores, secrets, and external exposure.

The selected unit separated the minimal response from the historical detailed
diagnostic response without preserving unsafe fields. `full=true` is an alias
only; it is not an authorization mechanism and cannot select the detailed view
by itself.

## Implemented boundary

The bounded implementation is present in these units:

- the `api.py:get_status` handler, limited to response selection and policy
  enforcement;
- `core/platform_status_access.py`, with no identity source and fail-closed
  server-side principal contract;
- `core/platform_status_schema.py`, with strict two-view validation and
  recursive sanitization;
- direct status consumers only: Overview, Hybrid and the provider panel's
  status-backed catalog loader.

Provider diagnostic callables, memory stores, runtime startup and hybrid-router
implementation remain outside the status route and were not changed.

When P1-A eventually starts, its status projection must use a generic
`domain_module_status` representation with parity across modules. The legacy
domain-specific branch currently observed in the diagnostic surface is a
`legacy singled-out domain status` debt item, not a privileged feature. The
migration must be versioned, consumer-tested, sanitized and reversible.

## Capabilities

- `platform_status.read_minimal`;
- `platform_status.read_detailed`.

The minimal view is intentionally usable for connection polling without an
identity source; the detailed capability is sufficient only for a server-side
principal accepted by the Owner/operator boundary. The default resolver is
unconfigured and therefore denies detail.
Neither capability grants write, runtime, execution, provider, integration,
secret, memory, log, metric, tenant, or root authority.

## Authorization order

Any future resolver extension must evaluate in this order and deny on any
missing or ambiguous result:

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

The minimal view contains only version, view, platform scope, bounded
status/liveness/readiness, running flag, explicit `DEFAULT_DENIED` and the
capability-gated detailed-view marker. It has no collections, provider names,
model names, health messages, filesystem paths, tool or agent inventory,
hybrid details, cycle limits, activity counts, tenant identifiers,
credentials, secrets or timing that enables meaningful reconnaissance.

The detailed view, if separately approved, remains Owner/operator-only and
must use an explicit allowlist. It must redact internal paths, secret-bearing
configuration, credentials, tokens, private prompts, tenant content, and
unbounded provider diagnostics. The projection must not copy raw memory, logs,
or metric payloads into status.

Status has no pagination contract. The current minimal view has no
collections. Any future detailed collection must have an explicit bound and
ordering contract before implementation; line-count, list size, or `full=true`
cannot replace authorization.

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

Identity, deployment and external-exposure gates remain inactive; internal
remediation is complete and the route remains externally default-denied:

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

External exposure remains `DEFAULT_DENIED`. Internal remediation is complete,
but no identity/deployment gate is activated and no productive external
exposure is declared.

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

Rollback must be a local, reviewable revert of the status unit and must
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

The selected unit is complete because the code diff is limited to the approved
status boundary, positive and negative tests pass, local consumers are
compatible, external exposure remains denied, and the checkpoint records
rollback and validation evidence. A green test result is not permission to
expose the route.

Until then, the only valid state is:

`P1-A_PLATFORM_STATUS_HEALTH_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
`INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
`EXTERNAL_EXPOSURE_DEFAULT_DENIED`

## Current roadmap cursor after Macro 04.3

Macro 04.3 completed the bounded internal P1-A status remediation and left the
next subfamily as a selection-only cursor:

`P1-B_PROTECTED_MEMORY_SELECTED_NOT_STARTED`

P1-C and P1-D remain `DEFERRED_NOT_STARTED`; no next subfamily was
implemented. The prior Macro 04.1 pause and Macro 04.2 release states remain
historical context. All activation gates remain inactive and external exposure
remains `DEFAULT_DENIED`.
