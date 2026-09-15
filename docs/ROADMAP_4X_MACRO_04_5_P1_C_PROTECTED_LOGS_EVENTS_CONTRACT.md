# Protected Logs and Events Contract - `protected_logs.v1`

## Purpose

P1-C replaces the legacy raw log viewer with a protected, structured,
sanitized, bounded, capability-gated, platform-scoped read surface. It is an
internal contract only. It does not create production authentication,
tenancy, retention, runtime, provider, support, export, or external exposure.

## Authority and capability

The only read capability is:

```text
observability.logs.read_sanitized
```

Identity is resolved server-side. Client headers, query identity, Origin, Host,
User-Agent, Forwarded, loopback, localhost, filesystem ownership, Owner-native
badges, plan, or UI state never grants authority. Wildcards and casing variants
are invalid.

The resolver is intentionally unconfigured in the current repository. Until a
trusted identity source exists, the route returns `503 LOG_ACCESS_UNAVAILABLE`.
A trusted principal without the exact capability returns `403
LOG_CAPABILITY_DENIED`. A tenant-shaped or otherwise unowned scope returns a
non-enumerative `404 LOG_SCOPE_UNAVAILABLE`.

## Request contract

Allowed query parameters are:

```text
view: summary | events
limit: integer 1..100; default 25
tenant_id: accepted only to return non-enumerative scope denial
```

The legacy `lines` parameter, paths, file names, regexes, grep expressions,
raw queries, arbitrary offsets, source selectors, executable expressions, and
unknown parameters return `400 LOG_QUERY_INVALID`. Invalid input is rejected
before any source read.

## Required access order

```text
NORMALIZE_REQUEST
-> RESOLVE_TRUSTED_PRINCIPAL_SERVER_SIDE
-> AUTHORIZE_CAPABILITY
-> RESOLVE_SERVER_CONTROLLED_SOURCE
-> VERIFY_SCOPE
-> READ_BOUNDED_SOURCE
-> PARSE_TO_STRUCTURED_EVENTS
-> EXPLICIT_ALLOWLIST_PROJECTION
-> CONTENT_REDACTION
-> CONTROL_CHARACTER_NORMALIZATION
-> DEFENSE_IN_DEPTH_SANITIZATION
-> BOUNDED_RESPONSE
```

Central invariant:

```text
ZERO_SOURCE_READ_ON_DENY
```

Denial cannot open files, stat paths, check existence, enumerate directories,
read events, consult stores, reveal source-dependent timing, invoke providers,
activate runtime, or execute work.

## Versioned envelope

Every successful response contains exactly:

```text
contract_version
view
scope
status
external_access
content_exposed
bounded
data
```

The fixed markers are:

```json
{
  "contract_version": "protected_logs.v1",
  "scope": "platform",
  "external_access": {"policy": "DEFAULT_DENIED", "enabled": false},
  "content_exposed": false,
  "bounded": true
}
```

## Summary view

`view=summary` returns only bounded event count, warning count, error count,
allowlisted content classes, and projection name. It never returns a path,
file name, line, message, ID, tenant, trace, or source selector.

The classification vocabulary includes `RAW_LOG_MATERIAL`, which is never
returned by either successful view.

## Events view

`view=events` returns at most 100 structured events. An event may contain only:

```text
timestamp
severity
category
outcome
code
message
```

Timestamp is included only when it matches the safe normalized form. Severity
is one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Category is one of
the documented classification values. Outcome is `observed`, `warning`, or
`failed`. Code is included only when safe and explicitly recognized. Message
is plain text, bounded to 280 characters, redacted, normalized, and HTML-safe.

## Server-controlled bounded reader

The current reader opens only the configured server path and reads at most 512
KiB from its end. It does not load an unbounded file, follow client selectors,
write, rotate, truncate, delete, export, or back up. It handles absent, empty,
rotated/truncated, very long, and invalid-encoding sources without exposing
source details. Invalid encoding is replaced in the projection and marked as
degraded through a safe event.

No path is returned to the client. Symlink and path-traversal authority cannot
be selected by the client because the source is not a request parameter; future
deployment hardening must still keep the configured log root server-controlled.

## Redaction and normalization

The projection uses allowlist-first selection and defense-in-depth sanitization.
Synthetic canaries cover authorization and bearer tokens, API keys, passwords,
cookies, session tokens, private keys, connection strings, credentialed URLs,
query secrets, email, phone, PII, prompts, payloads, model responses,
provider/model names, Windows/Linux paths, tracebacks, embedded JSON,
multiline messages, ANSI/control characters, CRLF injection, HTML, JavaScript,
casing variants, nested objects/lists, huge lines, and invalid encoding.

The original file is never rewritten. Redaction applies only to the response
projection.

## Error contract

```text
503 LOG_ACCESS_UNAVAILABLE
403 LOG_CAPABILITY_DENIED
404 LOG_SCOPE_UNAVAILABLE
503 LOG_SERVICE_UNAVAILABLE
400 LOG_QUERY_INVALID
```

Internal tracebacks, filesystem paths, exception objects, and provider details
are not returned.

## External and tenant boundary

```text
RAW_LOG_EXTERNAL_ACCESS: FORBIDDEN
EXTERNAL_ACCESS: DEFAULT_DENIED
TENANT_LOG_ACCESS: UNKNOWN_DEFAULT_DENY
OWNER_NATIVE: LINEAGE_ONLY_NOT_AUTHORITY
GLOBAL_OWNER_UNILATERAL_CONTENT_ACCESS: FORBIDDEN
```

Redaction is not a legal anonymization claim. Tenant ownership, retention, and
support access require separate future contracts and evidence.
