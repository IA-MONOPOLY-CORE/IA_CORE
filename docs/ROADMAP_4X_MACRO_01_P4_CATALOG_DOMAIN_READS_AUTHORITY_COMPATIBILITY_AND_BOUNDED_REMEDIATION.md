# Roadmap 4.x Macro 01 - P4 Catalog Domain Reads

## Contract identity

- Mission: `ROADMAP_4X_MACRO_01_P4_CATALOG_DOMAIN_READS_AUTHORITY_COMPATIBILITY_AND_BOUNDED_REMEDIATION`.
- State: `SELECTED_FUTURE_CONTRACT_NOT_STARTED`.
- Parent decision: `B7_ACCEPTED_WITH_EXPLICIT_LIMITS`.
- Selection authority: `DIRECTION`; preparation delegated to `ARCHITECTURE`.
- Active implementation state for all seven routes:
  `DEFERRED_TO_4X_BY_EXPLICIT_DIRECTION`.
- Policy: `DEFAULT_DENY_UNTIL_REQUIRED_EVIDENCE_EXISTS`.

This is a future entry contract. It does not call, expose, adapt, migrate,
retire or remove any route. It does not change HTML, JavaScript, i18n,
backend, payload, runtime, execution, providers, stores or integrations.

## Why P4 is first

P4 contains seven GET routes, has no direct destructive operation and provides a
bounded read surface for catalog and domain navigation. It offers an early
test of identity, tenant, visibility and compatibility without opening the
higher-risk settings, provider, workforce or materialization families. This
selection is a policy choice, not evidence that the routes are safe to expose.

## Exact route membership

| Route ID | Method | Path | Adopted policy | Required first gate |
| --- | --- | --- | --- | --- |
| `api_catalog_domain_creation_get` | GET | `/api/catalogs/domain-creation` | `KEEP_AS_COMPATIBILITY_SURFACE` | catalog audience and authorization |
| `api_catalog_roles_get` | GET | `/api/catalogs/roles` | `KEEP_AS_COMPATIBILITY_SURFACE` | catalog audience and authorization |
| `api_catalog_specializations_get` | GET | `/api/catalogs/specializations` | `KEEP_AS_COMPATIBILITY_SURFACE` | catalog audience and authorization |
| `api_domains_list_get` | GET | `/api/domains/list` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | domain visibility, deployment and tenant scope |
| `api_domain_profile_catalog_get` | GET | `/api/domains/{domain_id}/profile-catalog` | `KEEP_AS_COMPATIBILITY_SURFACE` | domain ownership and visibility |
| `api_domain_agent_presets_get` | GET | `/api/domains/{domain_id}/agent-presets` | `CONTAIN` | workforce/provider metadata scope |
| `api_domain_agent_preset_match_get` | GET | `/api/domains/{domain_id}/agent-presets/match` | `CONTAIN` | matching authority and scope |

The seven rows must remain complete and unique. No P1-P3 or P5-P9 route may
enter this block.

## Required authority contract

Before implementation or external exposure, the future mission must prove:

1. trusted identity, authentication and route authorization;
2. tenant identity, resource ownership and cross-tenant isolation;
3. intended audience for global catalogs and tenant domain metadata;
4. catalog/domain visibility rules, including inactive or hidden entries;
5. treatment of provider, model, workforce and other sensitive metadata;
6. exact request/response compatibility with the legacy surface;
7. external-consumer inventory and a version/deprecation policy;
8. payload and response ownership without inventing payload v2;
9. a named functional owner and a separate authority owner;
10. a recovery owner even though this block is read-only by design.

Required gates are `G01_IDENTITY_SOURCE`, `G02_AUTHENTICATION`,
`G03_AUTHORIZATION`, `G04_TENANT_ISOLATION`, `G05_CORS_TRUSTED_ORIGINS`,
`G06_INGRESS_HOSTING`, `G13_PROVIDER_CREDENTIALS` when metadata requires it,
`G18_EXTERNAL_CONSUMER_COMPATIBILITY` and `G19_PAYLOAD_RESPONSE_CONTRACT`.
Missing evidence means `REMAIN_DISABLED_OR_CONTAINED`.

## Negative bypass tests

The future mission must reject:

- anonymous, wrong-audience, wrong-role and expired identities;
- cross-tenant domain IDs, list filters and preset lookups;
- hidden, inactive or unauthorized catalog metadata;
- provider or workforce fields that are not approved for the audience;
- unknown consumers, incompatible response shapes and silent retirement;
- calls that bypass the selected bounded authority into another family;
- any route that turns a read contract into a write, activation or execution.

## Bounded implementation criteria

Each route may be kept as the compatibility surface, contained internally or
remediated only after the entry gates pass. The future mission must choose one
criterion per route and record it before changing code:

| Criterion | Permitted meaning |
| --- | --- |
| `KEEP_AS_COMPATIBILITY_SURFACE` | Preserve the existing contract while the bounded owner and gates are evidenced. |
| `CONTAIN` | Keep the route behind a documented non-public or non-authoritative boundary without pretending it is a successor. |
| `REMEDIATE` | Implement only the approved seven-route boundary with compatibility and negative bypass proof. |

No route may be labeled remediated merely because a canonical registry exists.
No route may gain a successor, adapter or migration without a separately
approved implementation station.

## Rollback and stop conditions

Rollback owner: `ROUTE_COMPATIBILITY_OWNER`, with
`STORAGE_AND_RECOVERY_OWNER` consulted if any persistent fixture or state is
introduced. The future mission must stop before implementation if identity,
tenant, visibility, compatibility, payload, provider metadata or owner evidence
is absent; if a second family is needed; if a protected surface changes; if a
negative bypass test cannot be expressed; or if rollback is only hypothetical.

Protected surfaces include all P0/P1/P3 matrix, widgets contract-aware,
Request Draft Panel, unrelated route families, payload v2, new endpoints,
runtime, execution, providers, workforce, secrets, live stores, DNS, HTTP,
sockets, integrations, HTML, JavaScript and i18n.

`ROADMAP_4X_MACRO_01_P4_CONTRACT_PREPARED_NOT_EXECUTED`
