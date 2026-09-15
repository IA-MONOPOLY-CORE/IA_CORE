# Roadmap 4.x Macro-Mission 04.3

## P1-A Platform Status Health contract

### Resulting boundary

`GET /api/status` is a versioned, two-level, domain-neutral read. The default
view is a bounded local lifecycle projection. `GET /api/status?full=true` is a
compatibility alias for the detailed view and never grants authority by itself.
The route does not call providers, models, domains, memory, tools, Hybrid
Router or runtime services.

### Minimal view

The minimal response has this exact top-level shape:

```json
{
  "schema_version": "platform_status.v1",
  "view": "minimal",
  "scope": "platform",
  "status": "available",
  "liveness": "available",
  "readiness": "available",
  "running": true,
  "external_access": {"policy": "DEFAULT_DENIED", "enabled": false},
  "detailed_view": "capability_gated"
}
```

The actual state is derived only from the local Supervisor lifecycle flag. No
`healthy` claim is made from the fact that HTTP answered. The response has no
collections and therefore cannot enumerate providers, agents, tools, domains,
paths, memory, activity, tenant data or timing information. `None`, a failed
local lifecycle read and a stopped Supervisor remain distinct as
`not_available`, `degraded` and `initializing` where applicable.

### Detailed view

The detailed view is emitted only after a server-side principal satisfies
`platform_status.read_detailed` for audience `ia-core-private-beta`. The
default resolver is deliberately unconfigured and returns sanitized `503`
`PLATFORM_STATUS_ACCESS_UNAVAILABLE`; no client header, query value, origin,
host, User-Agent or loopback appearance can replace that resolver.

The detailed response has the exact top-level fields validated by
`core/platform_status_schema.py`:

- version, view, scope, status, liveness and readiness;
- running and external access policy;
- a bounded fixed list of generic component states;
- an aggregate failure summary;
- explicit compatibility markers for the minimal route and `full=true` alias.

Components are `http_api`, `supervisor`, `domain_modules` and
`hybrid_exposure`. They are all at platform scope. Domain modules are a
generic position; Lotería has no top-level status field or inherent privilege.
`domain_modules` is `not_observed` and Hybrid exposure is `default_denied` in
this bounded mission. No active health check is implied.

### Access, sanitization and failure rules

`core/platform_status_access.py` defines a small fail-closed boundary without
implementing an identity provider. The principal is accepted only as a
server-injected typed value with an exact audience and capability set.

`sanitize_platform_status_value` recursively removes secret-bearing, path,
provider, model, agent, tool, memory, tenant, prompt, payload and raw-error
keys. Unsafe scalar values and unsupported objects are redacted. The strict
schema validator rejects unknown fields, cross-view fields, duplicate
components, invalid states, and any enabled external-access marker.

Each local component read is isolated. A broken lifecycle property produces a
safe `degraded/state_unreadable` component and does not fail the full detail
response. Status reads do not record events, update runtime metrics, write
files, load models, make network calls or mutate application state.

### Capabilities and non-authority

The names `platform_status.read_minimal` and `platform_status.read_detailed`
are canonical status capabilities. Minimal polling remains available as a
non-sensitive bounded liveness/readiness read. The detailed name is enforced
only through the server-side resolver. Neither capability grants write,
runtime, execution, provider, integration, secret, memory, log, metric,
tenant, root or external authority.

### Compatibility decision

The connection poller continues to use only `/api/status`. Overview consumes
only the minimal fields. Hybrid retains `full=true` as a detail request but
renders generic status components and a safe denial state. The Providers panel
no longer treats `/api/status` as a provider catalog and reports that the
catalog is not exposed by this status surface. No new endpoint was needed.
