# Roadmap 4.x Next Family Entry Contract - P1

## Contract state

`SELECTED_NOT_STARTED`

This is a future entry contract. Macro-Mission 03 does not execute its first
station and does not start Macro-Mission 04.

## Exact family and routes

Family: `P1_STATUS_OBSERVABILITY_MEMORY`

1. `GET /api/status`
2. `GET /api/memory`
3. `GET /api/logs`
4. `GET /api/metrics/dynamic`

The family contains four reads and no declared mutations. The route decision
source remains the authority for its historical dispositions and gate IDs.

## Baselines and objective

- Selection baseline: `2969ed469ed482968b4db4deac7b35a855f635e2`.
- Future execution baseline: must equal the published Macro 03 final HEAD at
  the next preflight; it is intentionally not invented here.
- Objective: establish a bounded, provider-independent internal read boundary
  for P1 only, with explicit identity, audience, authorization, tenant,
  redaction, retention and compatibility evidence.
- Required external state throughout: `REMAIN_DISABLED_OR_CONTAINED`.

## Reason and risks

P1 is selected because it combines high disclosure risk and architectural
centrality with existing internal observability, memory and audit contracts.
The risks are status/provider metadata leakage, cross-tenant memory reads,
secret-bearing logs, unbounded retention, metric audience confusion and
unknown external consumers. The future work must narrow those risks without
turning local principals into production identity.

## Gate contract

Internal gates to prove in a future mission: G01, G02, G03, G04, G08, G10,
G11 and G18, plus G06 for the status route if any deployment interpretation
appears. G19 remains a compatibility check even though it is not listed on the
historical P1 route rows. External gates remain inactive: no identity provider,
authentication deployment, tenant membership source, ingress, hosting, log
retention service, external consumer or production compatibility claim is
authorized by this contract.

## Authorized and prohibited surfaces

Future authorized surfaces are limited to the four P1 route boundary, directly
owned P1 internal modules, documentary evidence and tests required to prove the
boundary. A future station may not assume that permission here grants access
to a provider or persistent product store.

Prohibited: all other families; P0; P3 matrix; P4 code and routes; P5-P9
product code; HTML/CSS/contractual JavaScript/i18n; payload v2; runtime;
execution; providers; integrations; stores; secrets; CORS; hosting; public
exposure; workforce activation; real authentication; real external calls;
production readiness; Macro-Mission 04 within Macro 03.

## Required tests

Positive tests must cover only the exact four routes, controlled internal
principals, exact audience/capability, tenant-scoped memory, sanitized logs,
bounded metrics, stable existing payloads, no state mutation and no cross-request
identity contamination. Negative tests must cover anonymous and wrong-audience
requests, forged client identity, wrong capability, cross-tenant identifiers
and lists, nested secret-shaped data, retention/ownership absence, provider or
network activation, and any external exposure attempt.

## Stop and rollback

Stop if identity, tenant ownership, redaction, retention, consumer inventory,
payload authority or route ownership cannot be demonstrated; if a provider,
secret, network, product store, runtime or hosting change is required; if any
other family is touched; or if a real full-suite regression appears.

Rollback must be limited to the future P1 station commit(s), leaving the
published P4 boundary, route matrix and Macro 03 evidence intact. No reset,
rebase, merge, amend, squash or force-push is authorized.

## Future station shape and expected result

1. preflight and route-owner evidence;
2. P1 internal contract and bounded route guard;
3. adversarial P1 E2E checkpoint;
4. documentary closeout and publication.

Provisional future result: `ROADMAP_4X_P1_INTERNAL_READ_BOUNDARY_CLOSED_EXTERNAL_EXPOSURE_DEFAULT_DENIED`.
The exact mission token must be confirmed by that future prompt, not inferred
from this contract. A post-boundary E2E checkpoint is **required** because
identity, tenant isolation, redaction and retention are coupled read risks.

## Directional estimate

| Scenario | Effective Codex hours | Operator calendar | External dependencies | Internal readiness | Production readiness |
| --- | ---: | --- | --- | --- | --- |
| Accelerated | 8-14 | 2-5 days | none for bounded internal work; review latency low | possible after all gates/tests | not established |
| Central | 14-28 | 1-3 weeks | normal Direction review and possible guard repair | target after 3-5 missions | not established |
| Conservative | 28-50 | 3-8 weeks | identity/tenant/retention evidence or a second frontier may block | may remain contained | not established |

These are directional planning bands derived from P4 evidence, not promises,
dates, quota conversions or production forecasts.

`P1_STATUS_OBSERVABILITY_MEMORY_SELECTED_NOT_STARTED`
