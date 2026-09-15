# Roadmap 4.x Macro-Mission 04.4

## P1-B protected memory contract

### Contract identity

- Version: `protected_memory.v1`
- Route: `GET /api/memory`
- External exposure: `DEFAULT_DENIED`
- Current identity source: not configured; the default resolver returns `503 MEMORY_ACCESS_UNAVAILABLE`.
- Data policy: raw memory is never a response shape.

### Access order

Every future resolver extension must preserve this order:

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

No memory store method is called before principal and capability checks. Query
parameters, headers, origin, host, user agent, forwarded values, loopback and
`OWNER_NATIVE` are not identity or authority.

The denial invariant is `ZERO_READ_ON_DENY`: no denied request may call a
memory store method.

### Capabilities

```text
memory.metadata.read
memory.audit.read_sanitized
memory.tenant.read_sanitized
```

The capability names are exact, case-sensitive and server-side. Wildcards,
empty values and client-supplied capability strings are rejected.

### Views

`metadata` is the default representation. It may expose only a bounded memory
state, an aggregate record count, the contract version and the fixed content
classification labels. It does not expose keys, paths, values, prompts,
identifiers, samples, records or tenant names.

`audit` may expose only a bounded list of projected `status`, `started_at` and
`duration_ms` fields. Execution IDs, modes, agents, providers, prompts,
payloads, paths, errors and nested objects are excluded before sanitization.

`tenant` requires a future trusted principal, capability, server-side scope,
demonstrated ownership and demonstrated isolation. The current repository
does not prove those conditions, so the view returns non-enumerative
`404 MEMORY_SCOPE_UNAVAILABLE` without reading memory.

### Response shape

All successful views use the exact bounded envelope:

```json
{
  "contract_version": "protected_memory.v1",
  "view": "metadata",
  "scope": "platform",
  "status": "available",
  "external_access": {"policy": "DEFAULT_DENIED", "enabled": false},
  "content_exposed": false,
  "bounded": true,
  "data": {}
}
```

Unknown selectors and legacy `key`/`history_limit` queries return typed,
sanitized `400 MEMORY_QUERY_INVALID` errors. Errors contain only a code,
status, safe message and contract version. They never echo input, paths,
tracebacks, keys, tenant identifiers or content.

### Failure rules

| Condition | Response | Store reads |
| --- | --- | --- |
| No trusted principal | `503 MEMORY_ACCESS_UNAVAILABLE` | Zero |
| Missing view capability | `403 MEMORY_CAPABILITY_DENIED` | Zero |
| Tenant scope/ownership not proven | `404 MEMORY_SCOPE_UNAVAILABLE` | Zero |
| Store missing, corrupt or unreadable | `503 MEMORY_SERVICE_UNAVAILABLE` | Only after authorization |

There are no writes, provider calls, external calls, runtime activation,
model loading, promotions or execution side effects in this route.
