# Roadmap 4.x Macro-Mission 04.6 - P1-D Truth Matrix

## Mission identity

```text
MISSION: ROADMAP_4X_MACRO_04_6
SUBFAMILY: P1-D_PROTECTED_DYNAMIC_METRICS
PREVIOUS_MISSION: ROADMAP_4X_MACRO_04_5_P1_C
BASELINE: e9089eb1ad04ca0bca0d6b9806bca151c487e74e
BRANCH: main
EXTERNAL_EXPOSURE: DEFAULT_DENIED
```

This matrix records repository evidence before P1-D implementation. It does
not grant product authority, tenant authority, public exposure, or permission
to modify P1-A, P1-B, or P1-C.

## Route evidence

| Observation | Classification | Evidence | Consequence |
|---|---|---|---|
| `GET /api/metrics/dynamic` is registered in `api.py`. | `OBSERVED` | `api.py::get_dynamic_metrics` | Preserve method and path. |
| The legacy handler calls `_require_loteria()` before any identity or capability decision. | `OBSERVED` | Current handler source | Denial must move before domain resolution. |
| The handler reads `evolution.get_estadisticas_ciclo()`. | `OBSERVED` | Current handler source | Source read is protected by the new access boundary. |
| The handler reads domain V19 state when evolution is initialized. | `OBSERVED` | Current handler source | V19 state is not a protected payload field. |
| Legacy output contains `success`, `timestamp`, `forward_test`, `v19`, and `fase_actual`. | `OBSERVED` | Current handler source and Roadmap 4.x matrices | These fields are historical evidence, not compatibility promises. |
| The route computes domain-specific rates and relative advantage. | `OBSERVED` | Current handler source | Only a neutral, bounded aggregate may cross the new boundary. |
| A current UI caller was not found. | `OBSERVED` | Source audit and route/consumer matrix | No UI change is authorized or required. |
| External callers and deployment exposure are not demonstrated. | `UNKNOWN` | Repository evidence boundary | Keep external exposure default denied. |
| Metric owner is not demonstrated. | `UNKNOWN` | P1 family adjudication | Do not activate tenant access. |
| Tenant ownership and isolation are not demonstrated. | `UNKNOWN_DEFAULT_DENY` | P1 family adjudication | Reject tenant scope non-enumeratively. |
| Safe multi-tenant aggregation is not demonstrated. | `UNKNOWN_DEFAULT_DENY` | P1 family adjudication | Keep `tenant_metrics.read` inactive. |
| Retention, deletion, backup, and cost attribution are not demonstrated. | `FUTURE_CONTRACT_ONLY` | P1 sensitivity contract | Do not implement retention or attribution. |
| Public exposure is not authorized. | `EXTERNAL_EVIDENCE_REQUIRED` | P1 gate matrix | Remain `DEFAULT_DENIED`. |
| A versioned internal summary can be projected from synthetic source values. | `INFERRED` | P1-D contract to be tested | Use allowlist-first schema and adversarial tests. |

```text
ZERO_SOURCE_READ_ON_DENY: REQUIRED_INVARIANT
```

## Current route versus target boundary

| Dimension | Current legacy truth | P1-D target |
|---|---|---|
| Identity | Not demonstrated | Trusted server-side principal only |
| Audience | Not demonstrated | Exact `ia-core-private-beta` |
| Capability | None connected | Exact `observability.metrics.read_sanitized` |
| Tenant capability | None connected | `tenant_metrics.read`, future inactive |
| View | Implicit full legacy dictionary | `summary` only |
| Source | Lotería/evolution global state | Read only after access decision |
| Payload | Domain-shaped and timestamped | `protected_dynamic_metrics.v1`, neutral and bounded |
| Time | Exact request timestamp | Not exposed |
| Error behavior | Uncontracted 501/503 details | Versioned sanitized non-enumerative errors |
| Consumer | No UI caller demonstrated | No UI consumer introduced |
| External exposure | Deployment unknown | Default denied |

## GOKV / DOOL / OCI baseline

```text
TOTAL_ITEMS: 38
VALIDATED: 9
CANDIDATE: 22
PROMOTED: 7
DEVELOPMENT_ORIGIN_ITEMS: 22
NEW_CANDIDATE: NO_NEW_CANDIDATE
NEW_PROMOTION: NONE
NEW_WRITE: NONE
NEW_EVENT: NONE
NEW_PACK: NONE
OCI_RUNTIME_ACTIVATION: NONE
```

The execution metric is an operational evidence document, not a GOKV item and
not a promotion candidate.

## Hard frontiers

```text
METRIC_OWNER: UNKNOWN
TENANT_OWNERSHIP: UNKNOWN_DEFAULT_DENY
AGGREGATION_SCOPE: UNKNOWN_DEFAULT_DENY
CORRELATION_SAFE_TIME: UNKNOWN_DEFAULT_DENY
RETENTION: FUTURE_CONTRACT_ONLY
EXTERNAL_CONSUMER: EXTERNAL_EVIDENCE_REQUIRED
TRUSTED_IDENTITY_RESOLVER: NOT_CONFIGURED_DEFAULT_DENY
PROVIDER_ACCESS: NOT_IMPLEMENTED
RUNTIME_ACCESS: NOT_IMPLEMENTED
```

No frontier is filled with an assumption. A future mission must supply the
missing evidence before activating tenant or external access.
