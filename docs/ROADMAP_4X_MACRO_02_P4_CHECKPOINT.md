# Roadmap 4.x Macro-Mission 02 - P4 Bounded Internal Remediation Checkpoint

## Resultado

- Mission: `ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
- Baseline: `3c90529abf5e130624653a247084d773d6620dcb`
- Family: `P4_CATALOG_DOMAIN_READS`
- Branch: `main`
- Internal contract readiness: `COMPLETE_WITHIN_FROZEN_P4_SCOPE`
- External exposure readiness: `BLOCKED_DEFAULT_DENY`
- Production readiness: `NOT_AUTHORIZED`
- Macro-Mission 03: `NOT_STARTED`
- `VALIDATION_BASIS_HEAD`: `4a8b6a381a5c57e55286e4cd784a1e7f967996bd`
- Documentary closeout commit: identified externally after this record is committed.
- Post-fetch publication verification: identified externally after normal push and fetch.

This checkpoint closes the provider-independent internal boundary for exactly
the seven existing P4 GET routes. It does not connect an identity provider,
open production ingress, introduce public traffic, or change any surface
outside the approved `api.py` wiring, the single P4 access module, tests and
documentation.

## Frozen Route Contract

| Route | Required capability | Additional conditions | Disposition |
| --- | --- | --- | --- |
| `GET /api/catalogs/domain-creation` | `global_catalogs.read` | Authenticated principal and exact private-beta audience | Global catalog read |
| `GET /api/catalogs/roles` | `global_catalogs.read` | Authenticated principal and exact private-beta audience | Global catalog read |
| `GET /api/catalogs/specializations` | `global_catalogs.read` | Authenticated principal and exact private-beta audience | Global catalog read |
| `GET /api/domains/list` | `tenant_domains.read` | Valid tenant and explicit authorized-domain set; list is filtered | Tenant read |
| `GET /api/domains/{domain_id}/profile-catalog` | `tenant_domains.read` | Valid tenant and requested domain explicitly authorized | Tenant read |
| `GET /api/domains/{domain_id}/agent-presets` | `tenant_agent_presets.read_sanitized` | Valid tenant and requested domain explicitly authorized | Restricted sanitized read |
| `GET /api/domains/{domain_id}/agent-presets/match` | `tenant_agent_presets.read_sanitized` | Valid tenant and requested domain explicitly authorized | Restricted sanitized read |

The human boundary is separate from `core/agent_permission_contract.py`.
Professional roles in `catalogs/roles.json` do not grant human access. The
only capabilities introduced by this mission are:

- `global_catalogs.read`
- `tenant_domains.read`
- `tenant_agent_presets.read_sanitized`

The preset capability is intentionally specific: `tenant_domains.read` alone
cannot read presets or a preset match.

## Fail-Closed Semantics

The pure contract in `core/p4_request_access.py` validates the subject,
authentication flag, audience, tenant, capability set and authorized-domain
set before a protected registry read. The default dependency resolver is
unconfigured, so ordinary anonymous calls remain denied.

| Condition | Status | Normalized code |
| --- | ---: | --- |
| Resolver not configured | 503 | `P4_ACCESS_RESOLVER_NOT_CONFIGURED` |
| Missing, unauthenticated or malformed principal | 401 | `P4_PRINCIPAL_INVALID` |
| Wrong audience | 401 | `P4_AUDIENCE_INVALID` |
| Required capability absent | 403 | `P4_CAPABILITY_REQUIRED` |
| Invalid resource identifier or traversal-shaped identifier | 400 | `P4_RESOURCE_IDENTIFIER_INVALID` |
| Unauthorized, unlisted or cross-tenant domain | 404 | `P4_DOMAIN_NOT_AUTHORIZED` |
| Authorized principal with no domain IDs | 200 | Existing empty-list shape, with zero domains |

Unauthorized domain decisions are made before the registry read and use a
generic non-disclosing response. They do not echo the domain, tenant,
membership or configuration state.

## Tenant Isolation

The controlled-principal tests demonstrate that:

1. A principal carries one validated `tenant_id`.
2. `/api/domains/list` returns only IDs in the principal's explicit
   `authorized_domain_ids` set.
3. A domain record with a conflicting tenant is excluded from the list.
4. Direct access to an unlisted or other-tenant domain returns generic 404.
5. A missing authorized-domain set never grants domain access.
6. Invalid identifiers are rejected before state access; no empty, casing or
   traversal-shaped value creates an implicit grant.

No productive tenant store, membership store or identity provider was added.
The evidence uses FastAPI dependency overrides and controlled fixtures only.

## Preset Sanitization

Responses retain the current top-level envelope and sanitize each preset with
an explicit allowlist before HTTP serialization.

Allowed fields:

`id`, `role_id`, `specialization_id`, `nombre_visible`, `suggested_agent_id`,
`suggested_agent_name`, `short_description`, `decision_criteria`, `avoid`,
`orden`.

Excluded fields include `system_prompt`, `recommended_provider`,
`recommended_model`, `recommended_temperature`, `memory_policy`, `paper_seed`,
`activo`, secret references, operational instructions and every unknown field.
The private registry is not rewritten; only the response view is sanitized.
Tests serialize an intentionally sensitive preset and assert complete absence
of the excluded fields.

## Dual Gate Disposition

| Gate | Internal contract | External exposure |
| --- | --- | --- |
| G01 Identity source | Provider-independent contract ready | Blocked pending approved provider evidence |
| G02 Authentication | Fail-closed resolver and overrides verified | Blocked pending production authentication |
| G03 Authorization | Exact capability policy enforced | Blocked pending external operational mapping |
| G04 Tenant isolation | Controlled principals and filtering verified | Blocked pending production membership mapping |
| G05 CORS origins | Localhost-only behavior preserved | Blocked pending trusted-origin evidence |
| G06 Ingress/hosting | Not required for local closed tests | Blocked pending hosting and ingress evidence |
| G13 Provider credentials | Not required and not accessed | Blocked; provider integration not authorized |
| G18 External consumers | Local consumers protected; no external inventory invented | Blocked pending external inventory |
| G19 Payload contract | Successful status, keys, types and sanitized views tested | Blocked pending external compatibility evidence |

All nine gates remain inactive for external exposure. Internal readiness must
not be interpreted as production authorization.

## Validation Basis

Level A was run on `4a8b6a381a5c57e55286e4cd784a1e7f967996bd` and passed:

- Full repository suite: `6986 passed, 6 skipped, 5 warnings` in `1537.34 s`.
- Macro 02 focal suite: `20 passed` across the pure access and bounded-route tests.
- Historical relevant replay: `27 passed, 5 warnings` in `14.02 s`.
- Catalog/domain compatibility suite: `18 passed, 5 warnings` in `13.76 s`.
- Route census replay: `11 passed, 1 warning` in `10.79 s`.
- GOKV validation: `38` items, valid registry.
- JSON parse: `248` files valid.
- Secret policy: `20 passed, 1 warning`.
- `py_compile`: PASS.
- Node contractual checks: PASS.
- CORS baseline comparison: PASS, unchanged.
- Protected diff: PASS, zero forbidden files.
- `git diff --check`: PASS.

The full suite required two historical allowlist repairs after legitimate P4
code displacement. Each repair preserved the original assertions and scoped
the exception to its own checkpoint. The third full run is the valid green
basis above.

## Protected Boundary and Publication

No HTML, CSS, contractual JavaScript, i18n, unrelated backend, payload v2,
runtime, execution, endpoint family, integration, provider, secret, productive
store, P0, P1, P3 matrix, contract-aware widget or Request Draft Panel was
modified. CORS remains localhost-only. No network or external call occurred.

GOKV/DOOL/OCI were consulted and reconciled as `NO_NEW_CANDIDATE`; no vault
item was created or promoted. The stable publication protocol keeps the
validation basis separate from the documentary closeout and post-fetch remote
verification. Macro 03 is explicitly outside this execution.

`ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
