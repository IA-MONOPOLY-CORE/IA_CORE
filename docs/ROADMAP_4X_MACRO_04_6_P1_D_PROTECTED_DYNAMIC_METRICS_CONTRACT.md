# Roadmap 4.x Macro-Mission 04.6 - P1-D Protected Dynamic Metrics Contract

## Contract identity

```text
CONTRACT_VERSION: protected_dynamic_metrics.v1
ROUTE: GET /api/metrics/dynamic
ACTIVE_CAPABILITY: observability.metrics.read_sanitized
TENANT_CAPABILITY: tenant_metrics.read
TENANT_CAPABILITY_STATE: FUTURE_INACTIVE_UNTIL_OWNERSHIP_PROVEN
TENANT_SCOPE: UNKNOWN_DEFAULT_DENY
AUDIENCE: ia-core-private-beta
DEFAULT_VIEW: summary
ALLOWED_VIEW_NOW: summary
IDENTITY_SOURCE: TRUSTED_SERVER_SIDE_ONLY
EXTERNAL_ACCESS_POLICY: DEFAULT_DENIED
SOURCE_READ_ON_DENY: ZERO
RAW_DOMAIN_STATE_EXPOSED: NO
RAW_LEGACY_PAYLOAD_EXPOSED: NO
TIMESTAMP_EXPOSED: NO
UI_CHANGE: NOT_AUTHORIZED_AND_NOT_REQUIRED
ZERO_SOURCE_READ_ON_DENY: REQUIRED_INVARIANT
RETENTION: FUTURE_CONTRACT_ONLY
```

This is an internal, owner/operator-oriented contract. It is not a production
tenancy contract and does not activate a resolver that the repository does not
currently provide.

## Principal boundary

The only accepted principal shape is a server-injected immutable principal with
`subject_id`, `authenticated`, exact `audience`, an immutable exact capability
set, and optional `tenant_id`. Client headers, query values, cookies, origin,
host, referer, user agent, IP, forwarding headers, loopback, role names, and
legacy selectors are never authorities.

The active capability is case-sensitive and exact. Wildcards, extra
capabilities, inherited permissions, and `admin.read_all` are invalid. The
tenant capability is documented for a future contract only and is inactive.

## Fail-closed sequence

1. Normalize and validate query keys and the `summary` view.
2. Reject unknown selectors before identity and source access.
3. Resolve the principal only from the server-side boundary.
4. Validate principal shape, authentication, audience, and exact capability.
5. Reject tenant scope non-enumeratively before source access.
6. Resolve the legacy source and read its snapshot.
7. Project only the fixed neutral allowlist.
8. Validate the final response before returning it.

The denial path performs zero calls to `_require_loteria`,
`get_estadisticas_ciclo`, `get_v19_status`, providers, network, runtime,
execution, stores, memory, filesystem, writes, events, promotions, or model
loading.

## Response envelope

The exact envelope is:

```json
{
  "contract_version": "protected_dynamic_metrics.v1",
  "view": "summary",
  "scope": "platform",
  "status": "available",
  "audience": "ia-core-private-beta",
  "external_access": {"policy": "DEFAULT_DENIED", "enabled": false},
  "bounded": true,
  "aggregation": "bounded_internal_snapshot",
  "data": {
    "observation_count": 25,
    "observed_rate": 32.0,
    "relative_index": 1.45,
    "snapshot_status": "available",
    "projection": "allowlist_first_domain_neutral"
  }
}
```

The field names are semantically domain-neutral. The response contains no exact
timestamp, phase, version, reason, domain identifier, tenant identifier,
execution identifier, provider, model, prompt, payload, strategy, cost, or
raw source dictionary.

## Numeric and size rules

- Counts are integers in a fixed non-negative bounded range.
- Rates and indices are finite real numbers only; booleans, strings, `NaN`,
  positive infinity, negative infinity, negatives, and outliers are rejected.
- Precision is normalized deterministically.
- Unknown top-level, aggregation, data, and source-derived keys are rejected.
- Response serialization is measured using a synthetic fixture and recorded in
  the execution metric.
- Source failures become `DYNAMIC_METRICS_SERVICE_UNAVAILABLE` without source
  details.

## Error contract

```text
400 DYNAMIC_METRICS_QUERY_INVALID
403 DYNAMIC_METRICS_CAPABILITY_DENIED
404 DYNAMIC_METRICS_SCOPE_UNAVAILABLE
503 DYNAMIC_METRICS_ACCESS_UNAVAILABLE
503 DYNAMIC_METRICS_SERVICE_UNAVAILABLE
```

Every error is bounded, sanitized, versioned, and non-enumerative. Error
messages never contain paths, exceptions, source state, domain names, phase,
V19, providers, models, tenants, traces, secrets, or timestamps.

## Compatibility decision

The method and path remain unchanged. Legacy fields are not preserved because
there is no demonstrated consumer and their semantics disclose domain state.
No endpoint, payload v2, adapter, UI panel, HTML, CSS, JavaScript, or i18n
change is created.
