# Roadmap 4.x Macro-Mission 05 - Cross-Capability and Route Matrix

## Exact authority set

| Family | Canonical principal type | Active capability | Future/inactive capability | Allowed views |
|---|---|---|---|---|
| P1-A status | `PlatformStatusPrincipal` | `platform_status.read_detailed` | none | `full=true` detailed; minimal local view is intentionally unauthenticated |
| P1-B memory | `ProtectedMemoryPrincipal` | `memory.metadata.read`, `memory.audit.read_sanitized` | `memory.tenant.read_sanitized` | `metadata`, `audit`; tenant blocked |
| P1-C logs | `ProtectedLogsPrincipal` | `observability.logs.read_sanitized` | none declared | `summary`, `events` |
| P1-D metrics | `ProtectedDynamicMetricsPrincipal` | `observability.metrics.read_sanitized` | `tenant_metrics.read` | `summary` |

## Confusion rule

Each capability is valid only at its own boundary. Principal dataclasses are
nominally distinct and are not interchangeable. Wildcards, prefixes, suffixes,
case variants, whitespace variants, duplicate entries, Unicode confusables and
`admin.read_all` are rejected. Extra capabilities never widen authority.

The test matrix is the Cartesian product of the four active route boundaries
and all active, future and adversarial capability values. Every off-diagonal
entry must deny before source access. Future tenant capabilities remain
inactive even when present in a shaped synthetic principal.

## HTTP distinction preservation

Status detailed keeps its existing sanitized `503` resolver behavior. Memory,
logs and metrics preserve their existing `403` capability denial, `404` scope
denial and `503` resolver/service distinctions. Macro 05 does not normalize
codes merely for visual symmetry.

## Identity rule

Only server-side resolver output can reach an authorized branch. Headers,
cookies, query parameters, Origin, Host, User-Agent, Forwarded values,
loopback clients and request bodies are non-authoritative.
