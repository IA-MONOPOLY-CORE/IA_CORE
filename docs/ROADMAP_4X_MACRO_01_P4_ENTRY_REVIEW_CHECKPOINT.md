# Roadmap 4.x Macro 01 - P4 Entry Review Checkpoint

## Checkpoint identity

- Mission: `ROADMAP_4X_MACRO_MISSION_01_P4_ENTRY_AUTHORITY_COMPATIBILITY_AND_BOUNDED_REMEDIATION_REVIEW`.
- Family: `P4_CATALOG_DOMAIN_READS`.
- Baseline: `9a9a1820c9b1d769b950e6de9cb458f251cd215d`.
- Current local checkpoint before publication: four material commits after the baseline.
- Decision: `ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_COMPLETE_EXTERNAL_GATES_DEFAULT_DENIED`.
- Implementation state: `NOT_STARTED`.
- Exposure state: `NOT_AUTHORIZED`.
- Production readiness: `NOT_DECLARED`.
- Policy: `DEFAULT_DENY_UNTIL_REQUIRED_EVIDENCE_EXISTS`.

This checkpoint closes the entry review and prepares the next bounded plan. It
does not execute P4 remediation, expose a route, change product behavior or
reopen the accepted 3.x phase.

## Scope verified

The review covered exactly these seven read routes and no other family:

1. `GET /api/catalogs/domain-creation`
2. `GET /api/catalogs/roles`
3. `GET /api/catalogs/specializations`
4. `GET /api/domains/list`
5. `GET /api/domains/{domain_id}/profile-catalog`
6. `GET /api/domains/{domain_id}/agent-presets`
7. `GET /api/domains/{domain_id}/agent-presets/match`

The full route/source/payload/consumer record is in
`ROADMAP_4X_MACRO_01_P4_ROUTE_SOURCE_PAYLOAD_AND_CONSUMER_MATRIX.json`.

## Current repository truth

- Catalog loaders read `areas.json`, `niches.json`, `roles.json` and
  `specializations.json`; baseline counts are `30`, `200`, `20` and `80`.
- Domain listing reads `domains/*/domain.json` and in-code theme presets. Two
  manifests exist, but both are internal/legacy/hidden under the default
  filter, so the current visible domain count is `0` and theme count is `4`.
- Loteria profile and preset artifacts are intentionally inactive/archived;
  active-only responses contain zero roles and zero presets.
- The handlers perform reads and validation only. No direct write, state
  mutation, provider call, network call, runtime, execution, activation or
  materialization was observed.
- Local UI references exist in `ui/web/domains.js` and `ui/web/index.html`; the
  current lower-console guard prevents the domain.js fetch paths from
  dispatching. Focused tests establish local contract behavior only.
- No external consumer inventory, deployment proof, identity source, tenant
  mapping or approved metadata audience exists in the repository.

## Authority and compatibility decision

The authority and visibility contract is documented in
`ROADMAP_4X_MACRO_01_P4_AUTHORITY_AND_VISIBILITY_CONTRACT.md`; the gate and
compatibility matrix is in
`ROADMAP_4X_MACRO_01_P4_COMPATIBILITY_AND_GATE_MATRIX.json`.

All nine applicable gates remain `EXTERNAL_EVIDENCE_REQUIRED`, inactive and
default-denied:

`G01_IDENTITY_SOURCE`, `G02_AUTHENTICATION`, `G03_AUTHORIZATION`,
`G04_TENANT_ISOLATION`, `G05_CORS_TRUSTED_ORIGINS`, `G06_INGRESS_HOSTING`,
`G13_PROVIDER_CREDENTIALS`, `G18_EXTERNAL_CONSUMER_COMPATIBILITY` and
`G19_PAYLOAD_RESPONSE_CONTRACT`.

The inherited route dispositions remain:

- three global/domain catalog reads: `KEEP_AS_COMPATIBILITY_SURFACE`;
- domain list: `BLOCK_UNTIL_EXTERNAL_EVIDENCE`;
- profile catalog: `KEEP_AS_COMPATIBILITY_SURFACE`;
- agent presets and exact match: `CONTAIN` because provider/workforce
  metadata and matching authority are not proven.

Local loader correctness, `GET` semantics, CORS configuration, active/status
filtering and TestClient success do not satisfy external authority or exposure
gates. No payload v2, successor route, silent retirement, new permission
semantics or action semantics is authorized.

## Learning consultation

GOKV/DOOL/OCI were consulted under the current precedence:

`SECURITY_PRIVACY_HARD_CONTRACTS` -> `CURRENT_MISSION_EXPLICIT_CONSTRAINTS` ->
`CURRENT_CANONICAL_ARCHITECTURE` -> `CURRENT_REPOSITORY_STATE` ->
`GOKV_OPERATIONAL_GUIDANCE`.

The applicable promoted guidance is evidence-before-closure, focal/group/
canonical/deep test policy, contract preservation, station-local commits,
real-diff commit semantics, callable-chain-not-authorized-route,
read-only-method-not-read-authz and true-hard-frontier. These refine the
current decision but introduce no distinct knowledge item:
`NO_NEW_CANDIDATE`.

## Next mission package

`ROADMAP_4X_MACRO_02_P4_BOUNDED_REMEDIATION_EXECUTION_PLAN.md` is ready for a
future mission. It requires external evidence intake before any product diff,
freezes the seven routes, defines conditional `KEEP/CONTAIN/REMEDIATE`, and
specifies positive/negative compatibility tests and local rollback.

Macro 02 must stop if it needs a second family, new endpoint, adapter, bridge,
migration, payload v2, provider/network call, tenant store, runtime,
execution, workforce activation or a protected-surface change.

## Protected boundary

No change was made to `api.py`, `core/`, `domains/`, catalogs, HTML, CSS,
JavaScript, i18n, payload, runtime, execution, providers, workforce, stores,
secrets, integrations, endpoints, P0, P1, P3 matrix, contract-aware widgets
or Request Draft Panel. No HTTP, DNS, socket, provider or external call was
made. Roadmap 3.x remains closed and internally consistent; P4 is reviewed but
not implemented.

## Validation protocol

The focal entry-review suite passed before this checkpoint commit. Final
validation after the checkpoint commit must include the full repository suite,
GOKV validation, JSON parsing, Python compilation, Node checks, sanity checks,
protected-diff checks and `git diff --check`. Publication is allowed only if
all required checks pass, the prohibited diff remains empty and the working
tree is clean.

The first post-checkpoint full-suite attempt found one historical continuity
failure only: `test_no_product_or_protected_surface_changed_from_macro_05_baseline`
did not yet allow the exact new Macro 01 documentary/test filenames. All
product/protected assertions remained intact. The repair commit `11fa2ee`
added only those exact filenames to the historical allowlist and documentary
context; the targeted replay passed (`1 passed, 1 warning`). The final full
suite must be rerun after that repair-record state and its result is part of
the mission close-out.

`ROADMAP_4X_MACRO_01_P4_ENTRY_REVIEW_CHECKPOINT_DOCUMENTED_EXTERNAL_GATES_DEFAULT_DENIED`
