# Roadmap 4.x Macro-Mission 04.5 - P1-C Truth Matrix

## Authority and scope

This matrix records the repository truth observed before the P1-C remediation.
The working tree, current code, tests, schemas, and published checkpoints are
the highest authority. This document does not grant runtime, provider,
network, tenant, support, retention, or external-exposure authority.

Mission baseline: `0d6b234a70bd1c882872e4be02b018bd6de09a64`.
Mission: `P1-C_PROTECTED_LOGS_EVENTS_METHOD_SANTI_VERIFIED_EVIDENCE_UPDATE`.

## Initial route observation

| Surface | Observed behavior | Risk | Classification |
|---|---|---|---|
| `GET /api/logs` | Read `config.LOG_DIR / api.log` using full `read_text` and returned a tail. | File content could be exposed and memory use was not bounded by source bytes. | `OBSERVED` |
| Response | Returned `path`, requested line count, raw `lines`, raw warning/error collections, and session events. | Paths, messages, prompts, payloads, tracebacks, secrets, PII, and operational details could cross the boundary. | `OBSERVED` |
| Query | Accepted a configurable legacy `lines` parameter and clamped it. | Clamping lines did not make the source or content safe. | `OBSERVED` |
| Session events | Returned the in-memory event objects without a versioned projection. | Event messages were not proven sanitized or allowlisted. | `OBSERVED` |
| Logs HUD | Called `/api/logs`, displayed the path, raw lines, warnings, errors, and event messages. | Browser surface repeated the backend exposure. | `OBSERVED` |
| Ownership | No trusted tenant ownership or isolation resolver was demonstrated. | Tenant-private material could not be safely scoped. | `OBSERVED` / `UNKNOWN` |
| Retention | No governed retention, rotation, deletion, or recovery contract was demonstrated. | Lifecycle, legal retention, and restore claims would be unsupported. | `UNKNOWN` |

## Source and consumers

| Item | Repository evidence | Disposition |
|---|---|---|
| Server-controlled source | `config.LOG_DIR / api.log` configured by the server. | Client cannot select a file, directory, path, URL, stream, provider, or device. |
| Session source | `session_events` in `api.py`. | Only sanitized event projections may cross the route. |
| Backend consumer | `get_logs` in `api.py`. | Versioned `summary` and `events` views only. |
| HUD consumer | `loadLogs` in `ui/web/admin-panels.js`. | Contract-aware structured events only. |
| Indirect calls | No provider/runtime/execution dependency is needed by the protected route. | No indirect activation permitted. |
| Writes and side effects | The route is read-only; no log mutation is part of P1-C. | No rotate, truncate, delete, export, or backup. |

## Data classification

The minimum classification set is:

```text
PLATFORM_EVENT_METADATA
SANITIZED_APPLICATION_EVENT
SANITIZED_SECURITY_EVENT
TENANT_PRIVATE_EVENT
AUDIT_EVIDENCE_EVENT
RAW_LOG_MATERIAL
UNKNOWN_UNCLASSIFIED_EVENT
```

`RAW_LOG_MATERIAL` is never exposed. `UNKNOWN_UNCLASSIFIED_EVENT` receives
maximum restriction. `TENANT_PRIVATE_EVENT` remains blocked because ownership
and isolation are not proven. A log is not automatically trusted evidence and
is not automatically inheritable knowledge.

## Contract boundary

Allowed capability:

```text
observability.logs.read_sanitized
```

Allowed views:

```text
view=summary
view=events
```

The response is `protected_logs.v1`, platform-scoped, bounded, and marked
`content_exposed=false` and `external_access.policy=DEFAULT_DENIED`.

Summary may expose only availability/degradation, bounded counts, safe
classification labels, and the declared projection. Events may expose only a
normalized timestamp when safe, allowlisted severity/category/outcome, a safe
code when explicitly recognized, and a bounded sanitized message.

## Sensitive material explicitly excluded

The projection excludes raw lines, paths, file names, selectors, directory
names, IDs, tenants, prompts, payloads, model responses, provider/model names,
tracebacks, headers, tokens, cookies, passwords, API keys, private keys,
connection strings, credentials, arbitrary JSON, HTML, JavaScript, ANSI
sequences, control characters, and unbounded multiline content.

## Source-read invariant

The route performs request normalization and trusted server-side identity and
capability checks before resolving or opening the log source. A denied request
does not open files, stat paths, check existence, enumerate directories, read
events, consult stores, invoke providers, activate runtime, or reveal timing
based on source state.

```text
ZERO_SOURCE_READ_ON_DENY
```

## Unknowns and external evidence

| Claim | Status | Required evidence |
|---|---|---|
| Production identity provider exists for this route | `UNKNOWN` | `EXTERNAL_EVIDENCE_REQUIRED` |
| Tenant ownership and isolation | `UNKNOWN_DEFAULT_DENY` | `EXTERNAL_EVIDENCE_REQUIRED` |
| Legal retention policy | `UNKNOWN` | `EXTERNAL_EVIDENCE_REQUIRED` |
| Redaction equals legal anonymization | `UNKNOWN` | Privacy/legal review required. |
| External log exposure | `DEFAULT_DENIED` | No current exposure authority. |
| Recovery, backup, SIEM, export, remote support | `NOT_IMPLEMENTED` | Future contract and separate authority required. |

## Protected surfaces

P1-A, P1-B, P1-D, P0, P3, P4, CORS, global auth, production tenancy,
payload v2, runtime, execution, providers, integrations, models, weights,
real stores, real memory, retention/rotation/deletion, widgets,
Request Draft Panel, Enterprise Foundry, Cyber Range, IA_CORE OS, Macro-Mission
05, and Cognitive Kernel families remain outside this mission.
