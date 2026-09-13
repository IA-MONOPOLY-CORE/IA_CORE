# Roadmap 4.x Macro-Mission 02

## Direction acceptance

- Mission: `ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
- Baseline: `3c90529abf5e130624653a247084d773d6620dcb`
- Family: `P4_CATALOG_DOMAIN_READS`
- Authority: `DIRECTION`
- Decision status: `ACCEPTED_FOR_BOUNDED_INTERNAL_REMEDIATION`
- External exposure status: `DEFAULT_DENIED`

Direction authorizes a provider-independent, internal and fail-closed human
access boundary for exactly seven existing GET routes. The boundary prepares a
private multi-company beta contract without integrating an identity provider,
opening production ingress or changing any external surface.

## Accepted policy

The only human capabilities in this mission are:

- `global_catalogs.read`
- `tenant_domains.read`
- `tenant_agent_presets.read_sanitized`

Global catalog reads require an authenticated principal, the private-beta
audience and `global_catalogs.read`. Tenant reads additionally require a valid
`tenant_id`, `tenant_domains.read` and an explicit authorized-domain set.
Preset reads require `tenant_agent_presets.read_sanitized` and return an
allowlisted view only. Domain access is never inferred from a role catalog,
empty parameters, casing, a header, a cookie or a default tenant.

The human boundary is separate from `core/agent_permission_contract.py`, which
remains an agent-capability contract. No human role is inferred from the
professional roles catalog.

## Fail-closed contract

- Unconfigured resolver: `503`, normalized as
  `P4_ACCESS_RESOLVER_NOT_CONFIGURED`.
- Missing, unauthenticated or malformed principal: `401`, normalized as
  `P4_PRINCIPAL_INVALID`.
- Wrong audience: `401`, normalized as `P4_AUDIENCE_INVALID`.
- Missing required capability: `403`, normalized as
  `P4_CAPABILITY_REQUIRED`.
- Invalid resource identifier: `400`, normalized as
  `P4_RESOURCE_IDENTIFIER_INVALID`.
- Unauthorized, cross-tenant or unlisted domain: generic `404`, normalized as
  `P4_DOMAIN_NOT_AUTHORIZED`; the response does not echo the domain or tenant.
- An authorized empty domain set remains a successful `200` with the existing
  empty collection shape.

## Frozen boundaries

The implementation may change only `api.py`, one internal P4 module, tests and
the documentary artifacts named by this mission. It must not modify UI, CORS,
HTML, CSS, contractual JavaScript, i18n, backend families outside the wiring,
payload v2, runtime, execution, providers, integrations, stores, secrets,
P0/P1/P3, widgets or Request Draft Panel. No external call or real secret is
needed or permitted.

The successful P4 payload keys, types, status semantics, active filtering and
read-only behavior remain protected. Preset responses preserve their current
top-level structure while removing operational and sensitive fields through an
explicit allowlist before serialization.

## Acceptance

This record accepts internal contract remediation only. It does not accept
authentication production readiness, trusted origins beyond localhost,
hosting/ingress, provider credentials, external consumers or public exposure.
Those gates remain blocked until independent external evidence exists.
