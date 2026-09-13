# Roadmap 4.x Macro 02 - P4 Bounded Remediation Execution Plan

## Plan identity

- Prepared by: Roadmap 4.x Macro 01 entry review.
- Target family: `P4_CATALOG_DOMAIN_READS`.
- Target mission: `ROADMAP_4X_MACRO_MISSION_02_P4_BOUNDED_REMEDIATION`.
- Entry baseline: `9a9a1820c9b1d769b950e6de9cb458f251cd215d`.
- Current state: `PLAN_READY_EXTERNAL_GATES_DEFAULT_DENIED`.
- Current mission state: `NO_REMEDIATION_EXECUTED`.
- Policy: `DEFAULT_DENY_UNTIL_REQUIRED_EVIDENCE_EXISTS`.
- Operating methods: `ONE_MATERIAL_STATION_ONE_COMMIT`, `LOCAL_ROLLBACK`,
  `TRUTH_BEFORE_SCALE`, `CONDITIONED_AUTONOMY`.
- Functional owner: `CATALOG_DOMAIN_OWNER`.
- Authority owner: `DIRECTION_UNTIL_EXPLICIT_DELEGATION`.
- Compatibility/recovery owner: `ROUTE_COMPATIBILITY_OWNER`.

This is an executable decision package for a future mission, not permission to
execute it now. Macro 02 must stop at entry if the external gates remain
unproven. It must not expand beyond the seven exact P4 GET routes.

## Entry verdict from Macro 01

The repository proves a local legacy contract, deterministic catalog/domain
loaders, active/status filtering, path safety and read-only handler behavior.
It does not prove a trusted caller identity, authentication, authorization,
tenant isolation, approved ingress, external consumer compatibility, payload
field ownership or provider metadata policy. The nine relevant gates therefore
remain `EXTERNAL_EVIDENCE_REQUIRED`, inactive and default-denied.

The first executable action of Macro 02 is evidence intake and gate
reconciliation. If any required artifact is missing, the mission may only
record the controlled unknown and leave the route in its inherited disposition.

## Frozen scope

The route set is complete and immutable:

1. `GET /api/catalogs/domain-creation`
2. `GET /api/catalogs/roles`
3. `GET /api/catalogs/specializations`
4. `GET /api/domains/list`
5. `GET /api/domains/{domain_id}/profile-catalog`
6. `GET /api/domains/{domain_id}/agent-presets`
7. `GET /api/domains/{domain_id}/agent-presets/match`

No P1, P2, P3, P5, P6, P7, P8 or P9 route may enter the mission. A need for a
second family is an immediate stop condition and requires a new Direction
decision.

## Route execution criteria

| Route | Inherited disposition | Candidate execution criterion | Default while gates are absent |
| --- | --- | --- | --- |
| `/api/catalogs/domain-creation` | `KEEP_AS_COMPATIBILITY_SURFACE` | Add only the approved caller/audience boundary around the existing areas/niches response, preserving keys and active filtering | Keep local/test-bound |
| `/api/catalogs/roles` | `KEEP_AS_COMPATIBILITY_SURFACE` | Add only the approved caller/audience boundary around the existing global role response, preserving keys and omissions | Keep local/test-bound |
| `/api/catalogs/specializations` | `KEEP_AS_COMPATIBILITY_SURFACE` | Add only the approved caller/audience boundary around the existing optional `role_id` contract | Keep local/test-bound |
| `/api/domains/list` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | Do not implement until visibility, deployment, tenant and consumer evidence all pass | Remain blocked |
| `/api/domains/{domain_id}/profile-catalog` | `KEEP_AS_COMPATIBILITY_SURFACE` | Add only approved domain ownership and caller boundary; preserve validation and status behavior | Keep contained/local |
| `/api/domains/{domain_id}/agent-presets` | `CONTAIN` | Keep non-authoritative and redact/withhold provider/workforce-sensitive metadata unless G13 and audience policy pass | Remain contained |
| `/api/domains/{domain_id}/agent-presets/match` | `CONTAIN` | Keep exact matching non-authoritative unless scope, metadata, compatibility and negative bypass proof pass | Remain contained |

No route is `REMEDIATE` by default. A future station may select
`REMEDIATE` only after recording a route-level evidence decision and a named
approval. Existing registry presence alone is not sufficient.

## Required entry gates

Macro 02 must reconcile `G01_IDENTITY_SOURCE`, `G02_AUTHENTICATION`,
`G03_AUTHORIZATION`, `G04_TENANT_ISOLATION`, `G05_CORS_TRUSTED_ORIGINS`,
`G06_INGRESS_HOSTING`, `G13_PROVIDER_CREDENTIALS`,
`G18_EXTERNAL_CONSUMER_COMPATIBILITY` and `G19_PAYLOAD_RESPONSE_CONTRACT`.
`G06` is required for domain discovery; `G13` is required for preset routes;
the other route-to-gate mappings are frozen in the Macro 01 matrix.

For each applicable gate, the future mission must record:

- accountable owner and functional owner;
- approved evidence source and timestamp;
- positive test and expected bounded result;
- negative bypass test and expected rejection;
- controlled unknowns and explicit stop condition;
- whether the gate allows `KEEP`, `CONTAIN` or `REMEDIATE` for each route.

No gate can be passed by a source-code assertion, a local `TestClient` call, a
fixture, a UI fallback, a static CORS setting or a catalog's `activo/status`
field alone.

## Future station sequence

### Station A - entry reconciliation

Read the Macro 01 matrix, authority contract, inherited route adjudication and
future gate register. Verify the branch/baseline, protected-surface diff, route
count and current response snapshots. No product file changes are permitted.

### Station B - authority and visibility acceptance

Attach the approved identity, authentication, authorization, tenant, origin and
ingress evidence. Define global catalog audience, domain ownership, hidden and
inactive visibility, and the allowed audience for preset metadata. If any item
is absent, record `EXTERNAL_EVIDENCE_REQUIRED` and stop before implementation.

### Station C - compatibility freeze

Inventory repository and external consumers, capture request/response samples,
freeze the seven path/method pairs, and approve the version/deprecation rule.
The current shape remains authoritative until this station accepts compatibility.
No payload v2, successor route or silent retirement is allowed.

### Station D - bounded implementation decision

For each route choose exactly one of `KEEP_AS_COMPATIBILITY_SURFACE`,
`CONTAIN` or `REMEDIATE`. Any route with missing authority, tenant, provider,
consumer or payload evidence remains `KEEP` or `CONTAIN`; it cannot be marked
remediated for convenience.

### Station E - implementation, only if explicitly authorized

Implement the smallest approved boundary in one material commit. Preserve the
existing handler path and response/error contract unless the compatibility
station explicitly approves a change. Add no new route, adapter, bridge,
migration, store, provider, runtime or execution path.

### Station F - negative proof and rollback

Run route-level positive and negative tests, protected-surface scans, full
focused suite, `py_compile`, Node check, `git diff --check`, and the repository
suite required by the mission. Validate that rollback returns to the pre-change
compatibility checkpoint and that no partial state remains. Stop on any
protected diff or negative bypass failure.

## Exact future product diff boundary

The following is a conditional candidate diff, not a current authorization:

- `api.py`: only existing P4 handler dependencies or boundary calls, if the
  approved identity/authorization contract requires them; no new endpoint and
  no unrelated handler change.
- `core/catalog_registry.py` and/or `core/domain_registry.py`: only the
  smallest existing-loader boundary needed to enforce the approved visibility
  and metadata policy; no new persistence, provider, tenant store or runtime.
- `tests/test_roadmap_4x_macro_02_p4_bounded_remediation.py`: positive,
  negative, response-compatibility and protected-surface tests.
- one future checkpoint/evidence/ledger document for the authorized station.

The exact files and line-level diff must be approved by the entry evidence
record before editing. HTML, CSS, JavaScript, i18n, payload schemas, runtime,
execution, providers, workforce, stores, secrets, integrations, DNS, HTTP
traffic and unrelated route families are never candidate files for this plan.

If a proposed change requires a new endpoint, adapter, bridge, migration,
payload v2, provider call, tenant store, runtime or execution path, stop and
return `ROADMAP_4X_MACRO_02_BLOCKED_WITH_EVIDENCE_PRESERVED`.

## Compatibility and payload rules

The future mission must preserve the following observed contracts unless a
separate Direction decision records otherwise:

- catalog creation: `success`, `areas`, `niches_by_area`;
- roles: `success`, `roles`, with inactive fields omitted;
- specializations: `success`, `specializations_by_role`, optional `role_id`
  filter and `400` for an invalid/unknown role;
- domain list: `success`, `domains`, `themes`, `total`;
- profile catalog: `success` plus validated catalog keys and `404` for a missing
  catalog;
- presets: `success` plus validated preset keys, with inactive presets omitted;
- exact match: `success`, `domain_id`, `preset` for a match and `404` with
  `detail` for no active exact match.

No new permission, confirmation, action, execution, runtime, tenant or
provider-authority field may be smuggled into an existing response. Sensitive
provider/model/system-prompt metadata must be explicitly classified before it
can be returned to any audience.

## Test package required before a future commit

Positive proof must cover valid approved identity, intended audience, exact
global/domain scope, active visibility, stable response keys, status codes,
local consumer behavior and route-family containment.

Negative proof must reject anonymous, malformed, expired, forged or wrong-
audience identities; same-tenant wrong-role access; cross-tenant domain IDs,
list filters and matches; hidden/inactive metadata; unapproved provider or
workforce fields; unknown consumers; incompatible shape/status changes; route
family escape; writes; activation; execution; runtime; payload v2; and silent
retirement.

The test suite must also assert that P0/P1/P3 matrix, contract-aware widgets,
Request Draft Panel, HTML, JavaScript, i18n, backend surfaces outside the
approved boundary and protected route families remain unchanged.

## Rollback

Rollback owner: `ROUTE_COMPATIBILITY_OWNER`; consult
`STORAGE_AND_RECOVERY_OWNER` only if a future test introduces persistent
fixtures or state. Rollback consists of reverting the one material station
commit through the approved local rollback procedure, restoring the prior
compatibility checkpoint, re-running the negative and protected-surface suite,
and preserving all evidence and ledgers. No reset, rebase, amend, merge or
force-push is permitted.

Rollback is mandatory if a response shape drifts, a protected file changes, a
negative bypass passes, a second family enters scope, a provider/network call
appears, or the resulting boundary cannot be explained by the approved
authority contract.

## Exit criteria for Macro 02

Macro 02 may close only when all of the following are true:

- the seven-route scope is intact;
- applicable external gates have approved evidence or the route remains
  explicitly contained/blocked;
- compatibility inventory and version policy are recorded;
- all positive and negative tests pass;
- no payload v2, new endpoint, adapter, bridge, runtime, execution, provider,
  workforce, store, secret, integration, HTML, JavaScript or i18n change is
  present;
- protected P0/P1/P3 matrix, widgets and Request Draft Panel are preserved;
- rollback is proven, not hypothetical;
- checkpoint, evidence and accountability ledger agree with Git.

Otherwise the mission closes as
`ROADMAP_4X_MACRO_02_BLOCKED_WITH_EVIDENCE_PRESERVED` or
`ROADMAP_4X_MACRO_02_COMPLETE_EXTERNAL_GATES_DEFAULT_DENIED`, as appropriate.

`ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN_READY`
