# Roadmap 4.x Macro-Mission 02

## Reconciled execution plan

- Mission: `ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
- Baseline: `3c90529abf5e130624653a247084d773d6620dcb`
- Family: `P4_CATALOG_DOMAIN_READS`
- Internal disposition: `AUTHORIZED_BOUNDED_REMEDIATION`
- External disposition: `DEFAULT_DENIED_UNTIL_REQUIRED_EVIDENCE_EXISTS`
- Method: `ONE_MATERIAL_STATION_ONE_COMMIT`

This plan supersedes the future-only entry plan from Macro 01.1 only for the
approved internal implementation. It does not authorize production exposure.
The Direction acceptance and dual gate matrix are the governing artifacts:

- `docs/ROADMAP_4X_MACRO_02_P4_DIRECTION_ACCEPTANCE.md`
- `docs/ROADMAP_4X_MACRO_02_P4_DUAL_GATE_MATRIX.json`

## Frozen route set

1. `GET /api/catalogs/domain-creation`
2. `GET /api/catalogs/roles`
3. `GET /api/catalogs/specializations`
4. `GET /api/domains/list`
5. `GET /api/domains/{domain_id}/profile-catalog`
6. `GET /api/domains/{domain_id}/agent-presets`
7. `GET /api/domains/{domain_id}/agent-presets/match`

No other route family, payload v2, adapter, bridge, store, runtime,
execution path, provider or integration may enter this mission.

## Access contract

The single internal module `core/p4_request_access.py` owns a pure human
principal model, decision result, normalized rejection causes, dependency
resolver and preset response sanitizer. It must not import or reuse
`core/agent_permission_contract.py`.

The default resolver is not configured and returns `503`. Tests inject a
controlled `P4Principal` using FastAPI dependency overrides. A valid principal
has a stable subject, authenticated state, exact private-beta audience,
capabilities, tenant where needed and an explicit authorized-domain set.

| Surface | Necessary capability and conditions |
| --- | --- |
| Three global catalogs | authenticated + audience + `global_catalogs.read` |
| Domain list | authenticated + valid tenant + `tenant_domains.read`; filter to explicit authorized IDs |
| Profile catalog | domain list conditions + authorized domain |
| Presets and match | domain conditions + `tenant_agent_presets.read_sanitized` |

The capability check is exact and no role from `roles.json` grants access.
Missing capability is `403`. Missing or invalid identity/audience is `401`.
Invalid IDs are safely rejected with `400`; unauthorized or cross-tenant
domains are generic `404` responses without existence details. An authorized
empty domain set returns the unchanged successful empty-list shape.

## Compatibility and sanitization

Existing successful route keys, types, active/status/visibility filtering and
read-only behavior remain protected. The domain list keeps `success`,
`domains`, `themes` and `total`; catalog and profile keys remain unchanged.
Preset top-level keys remain `schema_version`, `domain_id`, `nombre`,
`descripcion` and `presets`.

The serialized preset allowlist is:

`id`, `role_id`, `specialization_id`, `nombre_visible`, `suggested_agent_id`,
`suggested_agent_name`, `short_description`, `decision_criteria`, `avoid`,
`orden`.

The response excludes `system_prompt`, `recommended_provider`,
`recommended_model`, `recommended_temperature`, `memory_policy`,
`paper_seed`, `activo` and every unknown field. Internal registry artifacts are
not rewritten; sanitization happens before HTTP serialization.

## Station sequence

1. Decision and architecture: register Direction acceptance, plan and dual gate matrix.
2. Pure access: implement the module and unit tests.
3. P4 wiring: protect only the seven handlers, filter domains and sanitize presets.
4. Historical compatibility: adapt only anonymous P4 tests with dependency overrides and exact historical allowlists.
5. GOKV/DOOL/OCI: consult, record `NO_NEW_CANDIDATE` when applicable, and do not promote automatically.
6. Level A: focal, catalog/domain, security, historical, JSON, compile, Node, protected diff, diff-check and full suite.
7. Level B: create checkpoint/evidence/ledger, rerun bounded validation, commit docs, push normally and verify publication.

Each material station receives one independent commit. Prohibited Git
operations are force-push, rebase, merge, reset, amend, squash, tags and
history rewriting.

## Stop conditions

Stop and preserve evidence if tenant isolation cannot be demonstrated, a
successful contract cannot be preserved, a protected surface changes, a
negative bypass passes, a provider/secret/network path appears, or any change
outside this boundary is required. External provider, hosting and consumer
evidence remain external blockers, not reasons to expose the route by default.

## Exit result

Close as
`ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
only after all internal evidence and Level B publication checks pass. If a
stop condition is reached, close as
`ROADMAP_4X_MACRO_02_BLOCKED_WITH_EVIDENCE_PRESERVED`.
