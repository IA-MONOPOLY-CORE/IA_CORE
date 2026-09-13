# Roadmap 4.x Macro 01 - P4 Authority and Visibility Contract

## Contract state

- Mission: `ROADMAP_4X_MACRO_MISSION_01_P4_ENTRY_AUTHORITY_COMPATIBILITY_AND_BOUNDED_REMEDIATION_REVIEW`.
- Family: `P4_CATALOG_DOMAIN_READS`.
- State: `ENTRY_REVIEW_CONTRACT_DOCUMENTED_IMPLEMENTATION_NOT_AUTHORIZED`.
- Baseline: `9a9a1820c9b1d769b950e6de9cb458f251cd215d`.
- Policy: `DEFAULT_DENY_UNTIL_REQUIRED_EVIDENCE_EXISTS`.
- Missing-evidence action: `REMAIN_DISABLED_OR_CONTAINED`.
- Functional owner: `CATALOG_DOMAIN_OWNER`.
- Authority owner: `DIRECTION_UNTIL_EXPLICIT_DELEGATION`.
- Recovery owner: `ROUTE_COMPATIBILITY_OWNER`.

This document records what the current repository can prove about the seven
existing GET routes. It does not expose a route, change a handler, add an
adapter, create a successor, establish authentication, or declare production
readiness. A local response observed through `TestClient` is evidence of the
current test boundary only; it is not evidence of external authorization,
tenant isolation, hosting, ingress or consumer compatibility.

## Authority boundary

The seven routes are the complete and closed P4 set. They are read-only at the
handler level and have no direct filesystem write, state mutation, provider
call, network call, runtime start, execution, activation or materialization.
They still expose governed metadata, so read-only does not mean harmless or
public. Authority remains unproven until the required external gates pass.

The current code has no authentication or authorization dependency attached to
these handlers. CORS has a local explicit-origin default and rejects wildcard
configuration, but this is not an approved edge policy. The current default
domain listing filters demo, hidden, legacy and non-active manifests, but the
filter is a filesystem visibility rule, not a tenant policy.

No route may be called a canonical successor merely because a canonical
registry or loader exists. The existing legacy path is the compatibility
surface until Direction approves a separately evidenced implementation.

## Audience and visibility contract

| Surface | Intended audience to be evidenced | Current repository behavior | Authority gap |
| --- | --- | --- | --- |
| Global areas and niches | An approved caller selecting domain-creation metadata | Reads active catalog records and omits operational fields from the response | No identity, audience, tenant or authorization boundary |
| Global roles | An approved caller selecting a professional role | Returns 20 active role records without the `activo` field | No identity, audience, tenant or authorization boundary |
| Global specializations | An approved caller selecting a specialization, optionally by role | Returns 80 active records grouped by role; invalid role is `400` | No identity, audience, tenant or authorization boundary |
| Domain list | An approved caller allowed to discover visible domains in the deployment scope | Returns `0` visible domains at baseline and four theme presets; internal domains are excluded by default | No deployment, ingress, tenant or public-discovery proof |
| Domain profile catalog | An approved caller allowed to inspect one domain's profile options | Validates domain and cross-references global roles/specializations; inactive domain roles are omitted | No domain ownership, tenant mapping or authorization proof |
| Domain agent presets | An approved caller allowed to inspect bounded, non-active preset metadata | Validates against the domain profile catalog; inactive presets are omitted | Workforce/provider metadata may be present if an active preset is introduced; G13 is required |
| Exact preset match | An approved caller allowed to resolve one exact domain/role/specialization match | Returns `404` for the inactive Loteria placeholder and for no match | Matching authority, tenant boundary and metadata audience are unproven |

The baseline contains two domain manifests: `demo_generico` is demo/hidden and
`loteria` is legacy/hidden. Consequently `/api/domains/list` returns no visible
domains under its default filter. This is an observed state, not a guarantee
that future domain materialization is permitted.

## Identity, authentication and tenant requirements

Before any external exposure or behavior change, the future mission must
provide, at the same boundary:

1. an approved identity source, subject-to-tenant mapping and audience claim;
2. authentication validation and rejection behavior for missing, malformed and
   expired credentials;
3. capability and resource authorization for every route and metadata class;
4. an explicit rule for global catalogs versus tenant-owned domain metadata;
5. cross-tenant rejection tests for domain IDs, list filters and exact matches;
6. approved trusted origins and an ingress/deployment traffic scope;
7. a named owner for approval, denial, recovery and compatibility evidence.

Static source inspection cannot satisfy these requirements. Until they exist,
the routes remain local/test-bound or contained and no production exposure may
be claimed.

## Sensitive and operational metadata

The source schema for domain agent presets accepts `system_prompt`,
`recommended_provider`, `recommended_model`, `memory_policy` and `paper_seed`.
Those fields are metadata, not permission to invoke a provider, execute a model,
activate workforce or create an agent. The current Loteria preset is inactive,
has no status field, and is removed from active output; the observed active
response therefore contains zero presets and no provider fields.

Future implementation must choose and test a safe audience policy before an
active preset can expose any provider, model, prompt, workforce or memory
metadata. No credential value was read. No provider call, network call or
runtime path was executed in this review.

## Response and error authority

The existing response shapes are owned by `CONTRACT_AND_PAYLOAD_OWNER` in
coordination with `ROUTE_COMPATIBILITY_OWNER`. They must remain the baseline
for any future bounded work. No payload v2, new field, permission field,
confirmation field, action field, successor path or silent shape drift is
permitted in this entry review.

Observed error behavior is part of the legacy contract:

- shared catalog file/validation failures map to `500` with `detail`;
- an invalid or unknown specialization `role_id` maps to `400` with `detail`;
- a missing profile or preset catalog maps to `404` with `detail`;
- invalid domain/profile/preset data is classified as `400` or `500` according
  to the existing message-based handler logic;
- an exact match with no active preset maps to `404` with `detail`;
- `/api/domains/list` skips malformed/unreadable manifests and continues, or
  returns an empty list when its root is absent.

These observations are not an endorsement of message-based status mapping for
future public use. A future implementation may not change them without a
compatibility decision and negative tests.

## Consumer and version policy

Known repository consumers are `ui/web/domains.js`, `ui/web/index.html`, and
the focused tests in `tests/test_catalogs.py`, `tests/test_domains.py`,
`tests/test_domain_cleanup.py` and `tests/test_api_admin_panels.py`.
`domains.js` contains a read-only guard that prevents its catalog/domain fetch
paths from dispatching in the current UI state. `index.html` contains generic
profile fallback and preset-match references, not proof of an external client.

No external consumer inventory, request corpus, SDK contract, deprecation
policy or version negotiation evidence exists in the repository. Therefore
G18 remains externally blocked. The compatible policy for the next mission is:

- preserve the exact seven path/method pairs and current response/error shape;
- inventory known and unknown consumers before any route authority change;
- require explicit compatibility tests before adding, hiding or removing a
  field or changing status semantics;
- do not silently retire a path or invent a v2 path;
- use the existing path as the compatibility surface unless Direction approves
  a separately named version/deprecation decision.

## Route dispositions for the next mission

| Route | Disposition | Entry meaning | Default while evidence is missing |
| --- | --- | --- | --- |
| `/api/catalogs/domain-creation` | `KEEP_AS_COMPATIBILITY_SURFACE` | Preserve the local legacy contract while catalog audience and authorization are evidenced | Contained/local only |
| `/api/catalogs/roles` | `KEEP_AS_COMPATIBILITY_SURFACE` | Preserve global role response while audience and authorization are evidenced | Contained/local only |
| `/api/catalogs/specializations` | `KEEP_AS_COMPATIBILITY_SURFACE` | Preserve global role-filtered response while audience and authorization are evidenced | Contained/local only |
| `/api/domains/list` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | Do not treat filesystem discovery as deployment or tenant visibility | Remain blocked |
| `/api/domains/{domain_id}/profile-catalog` | `KEEP_AS_COMPATIBILITY_SURFACE` | Preserve validated domain read while ownership and scope are evidenced | Contained/local only |
| `/api/domains/{domain_id}/agent-presets` | `CONTAIN` | Keep provider/workforce-sensitive metadata behind a non-authoritative boundary | Remain contained |
| `/api/domains/{domain_id}/agent-presets/match` | `CONTAIN` | Keep exact matching non-authoritative until scope and metadata policy are evidenced | Remain contained |

## Negative boundary rules

The future mission must reject anonymous, wrong-audience, wrong-role, expired
and forged identities; cross-tenant IDs and filters; hidden/inactive metadata;
unapproved provider/workforce fields; unknown consumers; incompatible payloads;
silent retirement; route-family escape; writes; activation; execution; and any
claim that a read response grants permission. A UI fallback or local test
success cannot satisfy these negative gates.

## Stop and recovery conditions

Stop before implementation when any required external gate is absent, when a
second route family is needed, when a protected surface changes, when a
negative bypass test cannot be expressed, or when recovery is hypothetical.
The primary recovery owner is `ROUTE_COMPATIBILITY_OWNER`. If a future station
introduces persistent fixtures or state, consult
`STORAGE_AND_RECOVERY_OWNER` before proceeding. Rollback must restore the prior
compatibility checkpoint without deleting historical evidence.

Protected surfaces remain all P0/P1/P3 matrix, contract-aware widgets,
Request Draft Panel, unrelated route families, payload v2, new endpoints,
runtime, execution, providers, workforce, secrets, live stores, DNS, HTTP,
sockets, integrations, HTML, JavaScript and i18n.

`ROADMAP_4X_MACRO_01_P4_AUTHORITY_AND_VISIBILITY_CONTRACT_DOCUMENTED_DEFAULT_DENY`
