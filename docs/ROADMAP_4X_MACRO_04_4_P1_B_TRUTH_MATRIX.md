# Roadmap 4.x Macro-Mission 04.4

## P1-B Protected memory truth matrix

This matrix records only repository-observed behavior and the bounded
remediation in `protected_memory.v1`. Memory values, keys, prompts, paths and
real contents are intentionally not reproduced here.

| Surface | Observed read | Sensitivity | Consumer | Authority required | Ownership | Tenant scope | Side effects | Legacy behavior | Remediation decision | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `GET /api/memory` default | `MemoryManager.list_keys()`, history, selected value and orchestration detail | High: raw content, identifiers, prompts, possible secrets and PII | HUD Memory panel | None demonstrated | Unknown | Unknown | No write demonstrated | Raw unbounded snapshot | Replace with metadata view, capability-gated before any store read | `api.py`, historical route matrix |
| `GET /api/memory?key=...` | Client-selected key and value | High; selector was treated as a read address | HUD Memory panel | None demonstrated | Not proven | Not proven | Read only | Key enumeration and value dump | Reject legacy selector as typed `MEMORY_QUERY_INVALID` | `api.py`, UI consumer |
| `GET /api/memory?view=metadata` | Bounded count and lifecycle state after authorization | Medium/low operational metadata | Future authorized consumer | `memory.metadata.read` | Platform metadata only | No tenant content | Read only | Not available | Allow explicit metadata projection; no keys, paths or values | `protected_memory_schema.py` |
| `GET /api/memory?view=audit` | Bounded synthetic audit projection after authorization | Sanitized evidence only | Future authorized consumer | `memory.audit.read_sanitized` | Platform audit evidence | No tenant content | Read only | Not available | Allow status/time/duration fields only; omit IDs, agents and content | `protected_memory_schema.py` |
| `GET /api/memory?view=tenant` | No store read; scope is not demonstrated | Confidential enterprise memory | No active consumer | `memory.tenant.read_sanitized` plus proven ownership and isolation | Owning enterprise only | Unknown and therefore denied | None | No tenant contract | Return non-enumerative `MEMORY_SCOPE_UNAVAILABLE` | access tests |
| HUD Memory panel | Previously rendered keys, values, paths and raw history | High | `ui/web/admin-panels.js` | No browser-derived authority | Unknown | Unknown | No submit or mutation | Generic JSON dump | Render only protected state; disable key enumeration and show safe unavailable text | UI contract tests |

## Reconstructed route order

The route now follows:

```text
NORMALIZE_REQUEST
→ RESOLVE_TRUSTED_PRINCIPAL_SERVER_SIDE
→ AUTHORIZE_CAPABILITY
→ RESOLVE_SCOPE_SERVER_SIDE
→ VERIFY_OWNERSHIP
→ READ_MINIMUM_REQUIRED_DATA
→ EXPLICIT_ALLOWLIST_PROJECTION
→ DEFENSE_IN_DEPTH_SANITIZATION
→ BOUNDED_RESPONSE
```

`tenant` stops at scope/ownership because tenant isolation is not demonstrated
by the repository. The default resolver has no identity source and fails closed.

## Claim classification

- `OBSERVED`: the legacy handler read `MemoryManager` keys, history and selected values; the HUD consumed those fields.
- `OBSERVED`: the repository has no trusted memory principal resolver or demonstrated tenant isolation.
- `INFERRED`: orchestration history may contain business content, prompts, identifiers or provider-derived material.
- `UNKNOWN`: ownership, retention, legal classification, cryptographic custody and tenant boundary.
- `EXTERNAL_EVIDENCE_REQUIRED`: any production identity provider, external exposure, support access or recovery mechanism.
