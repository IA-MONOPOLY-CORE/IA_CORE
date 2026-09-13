# Roadmap 3.x Original Scope Evidence Coverage

## Identity

- Mission origin: `ROADMAP_3X_MACRO_MISSION_04_TRUE_COMPLETION_RECALIBRATION_EVIDENCE_COVERAGE_AND_CLOSURE_PATH`; closure: Macro 05.
- Evidence baseline: `43530e656066a3c40d9afb8a5a4a381b38f29f38`
- Authority: current repository plus published checkpoints; future documents
  are not capability evidence.
- Primary records: exactly one row for each original scope `3.0` through `3.9`.
- Companion register: [ROADMAP_3_X_TRUE_COMPLETION_GAP_REGISTER.json](C:/IA_CORE/docs/ROADMAP_3_X_TRUE_COMPLETION_GAP_REGISTER.json)

This document reconstructs the original 3.x scope as an evidence crosswalk. It
does not claim that every historical prompt with a similar number was a
single operational phase. The numbered rows below are the original macro
scope used by the completion contract:

`3.0` backend inventory; `3.1` contracts and payloads; `3.2` domains,
materialization and lifecycle; `3.3` agents, profiles, presets, papers and
teams; `3.4` memory, evidence and learning; `3.5` providers, model routing and
hardware awareness; `3.6` security, secrets and external actions; `3.7` tests
and quality debt; `3.8` master findings map; `3.9` executable remediation plan.

## Coverage vocabulary

### Primary state

Each row has one primary state from the true completion contract:

`AUDITED`, `DECIDED`, `REMEDIATION_READY`, `REMEDIATION_ENTRY_READY_NOT_IMPLEMENTED`, `REMEDIATED`, `ACTIVATED`,
`PRODUCTION_READY`.

### Coverage result

The row also has one evidence result:

`VERIFIED_COMPLETE`, `PARTIAL`, `MISSING`,
`NOT_APPLICABLE_WITH_ENFORCEABLE_GATE`, `EXTERNAL_EVIDENCE_REQUIRED`,
`DIRECTION_DECISION_REQUIRED`, `TRUE_HARD_FRONTIER`.

`VERIFIED_COMPLETE` means complete for the assigned documentary scope with
limits recorded. It never means production readiness. `DECISION_READY` in the
register is a separate readiness property and does not turn a recommendation
into a decision.

## Scope crosswalk

| Scope | Original responsibility | Primary state | Coverage result | B block / frontiers | Evidence conclusion | Remaining gap and legitimate owner |
| --- | --- | --- | --- | --- | --- | --- |
| `3.0` | Backend read-only terrain: routes, persistence, runtime/execution, providers, agents and trust boundaries. | `AUDITED` | `VERIFIED_COMPLETE` | B-1/B-3/B-4/B-5/B-6; F-001/F-002/F-003/F-007/F-008 | The elite audit has static source census, call-path, side-effect, runtime, provider, workforce and security graphs. | Deployment, live traffic and external authority remain outside static audit; hosting/security owners. |
| `3.1` | Security, permission, activation and trust-boundary audit for the legacy surface. | `AUDITED` | `EXTERNAL_EVIDENCE_REQUIRED` | B-1/B-4; F-001/F-002/F-003/F-007 | Local CORS, missing route-level auth evidence, secret-bearing settings and fail-closed activation gates are recorded. | Approved identity, tenant, CORS and deployed-edge evidence; Direction plus hosting/security. |
| `3.2` | Contracts, payloads, legacy API versus canonical control-plane coverage and route convergence. | `AUDITED` | `TRUE_HARD_FRONTIER` | B-2/B-3; F-004/F-005 | All 36 routes and 20 canonical controls are reconciled; no positive route adapter is demonstrated and every route destination remains `UNKNOWN`. | Direction must select policy before any authority-changing route work; selected route owner supplies compatibility evidence. |
| `3.3` | Domains, materialization and lifecycle ownership across legacy and contract surfaces. | `AUDITED` | `PARTIAL` | B-3/B-5/B-6; F-005/F-006/F-008/F-010 | Domain and sandbox materializer contracts, path containment and lifecycle gates are evidenced. | Product-store ownership, lifecycle authority and operational recovery are not demonstrated; domain/store owner. |
| `3.4` | Memory, evidence, learning, GOKV, DOOL and OCI governance. | `AUDITED` | `PARTIAL` | B-3/B-5/B-7; F-003/F-008 | Legacy memory and learning paths plus development-only append-only GOKV and PROMOTED_ONLY OCI are inventoried and validated. | Production retention, tenant ownership, live evidence ingestion and any promotion authority remain unproven; storage/governance owner. |
| `3.5` | Providers, credentials, model routing and hardware-aware selection. | `AUDITED` | `EXTERNAL_EVIDENCE_REQUIRED` | B-4/B-6; F-007/F-010 | NVIDIA and Ollama source-callable paths, routing/configuration and local hardware probes are documented; no provider call occurred. | Credential, egress, availability, cost and deployment evidence; provider/deployment owner. |
| `3.6` | Security, secrets and external-action boundary. | `AUDITED` | `EXTERNAL_EVIDENCE_REQUIRED` | B-1/B-4/B-5; F-002/F-003/F-007/F-008 | No secret values were read; dangerous primitives, settings write path, CORS wildcard and disabled runtime/external gates are recorded. | Approved policy, edge enforcement, rotation/retention and external-action authorization; Direction/security/deployment. |
| `3.7` | Tests, historical guards, hermeticity and quality-debt accounting. | `AUDITED` | `VERIFIED_COMPLETE` | B-0/B-7; F-000 | Macro 02.1/02.2 and Macro 03 preserve historical endpoints, negative guards, hermetic boundaries and a green published suite. | Final Macro 04 suite still must run after new documentary tests; test owner. |
| `3.8` | Master findings map across P0/P1/P2/P3 and all 12 frontiers. | `DECIDED` | `VERIFIED_COMPLETE` | B-1 through B-7; F-000 through F-011 | Direction accepted the findings and adopted the route policy; external evidence and implementation remain separately gated. | Preserve each governed gate and stop before authority-changing work. |
| `3.9` | Executable remediation plan for 4.x, ordered by distance to the first true hard frontier. | `REMEDIATION_ENTRY_READY_NOT_IMPLEMENTED` | `VERIFIED_COMPLETE` | B-7 / future 4.x entry; F-002/F-004/F-005/F-007/F-008/F-010/F-011 | Direction accepted the one-family plan shape and selected P4 as the future entry; no remediation is executed here. | Require all P4 entry gates and negative bypass evidence before implementation. |

## Findings before and after recalibration

| Area | Inherited Macro 03 position | Macro 04 recalibration |
| --- | --- | --- |
| B-0 authority/completion contract | Implicitly inherited; Macro 03 focused on B-7 readiness. | Explicit true completion equation and state machine are published. |
| B-1 / B-2 | `CLOSED_WITH_EXPLICIT_LIMITS`; unresolved trust and route authority. | Retained as audited boundaries; external and Direction requirements are named as gaps, not silently closed. |
| B-3 | `CONTRACT_READY`; canonical controls existed without route coverage. | Audited as a complete coverage finding; still not route remediation. |
| B-4 / B-5 / B-6 | `CONTRACT_READY`; runtime, provider, store and workforce activation absent. | Retained as audited contract boundaries with executable future gates. |
| B-7 | `B7_READY_FOR_DIRECTION_ACCEPTANCE`; Direction acceptance pending. | `B7_ACCEPTED_WITH_EXPLICIT_LIMITS`; no production or 4.x execution claim. |
| F-000 | Dissolved by historical endpoint convergence. | Remains dissolved; current Macro 04 tests are scoped separately. |
| F-001 through F-011 | Open/deferred as recorded by Macro 03. | No frontier is erased; each is assigned an owner, evidence requirement and next phase. |
| F-004 | Policy-level ambiguity dissolved; route-specific authority hard. | Direction adopted 36 policy dispositions; historical destinations remain `UNKNOWN` and implementation is explicitly deferred. |

## B-0 through B-7 recalibration

| Block | Before Macro 04 | After Macro 04 evidence package | Closure effect |
| --- | --- | --- | --- |
| B-0 | Inherited completion doctrine. | Explicit true completion contract and prohibited claims. | Enables auditable phase-exit test; does not close B-7. |
| B-1 | Closed with explicit limits. | Audited; external trust facts still pending. | Blocks authority-changing security work. |
| B-2 | Closed with explicit limits. | Audited; 36 route destinations remain unknown. | Blocks destination/remediation authority. |
| B-3 | Contract ready. | Audited coverage; positive route usage remains unproven. | Blocks route-to-canonical claim. |
| B-4 | Contract ready. | Audited; provider/runtime evidence remains external or future. | Blocks activation claim. |
| B-5 | Contract ready. | Audited; product ownership/restore remains unresolved. | Blocks operational write claim. |
| B-6 | Contract ready, no active workforce. | Audited; activation and deployment remain prohibited. | Blocks workforce claim. |
| B-7 | Direction decision pending. | Accepted with explicit limits. | Blocks production and implementation until future gates pass. |

## F-000 through F-011 disposition

| Frontier | Macro 03 status | Macro 04 treatment | Close condition |
| --- | --- | --- | --- |
| F-000 | `DISSOLVED` | Preserved as dissolved historical-test frontier. | Historical tests continue to use their own evidence endpoint. |
| F-001 | `OPEN` external evidence | `EXTERNAL_EVIDENCE_REQUIRED`; no deployment claim. | Approved edge, identity and traffic evidence. |
| F-002 | `OPEN` true hard | `TRUE_HARD_FRONTIER`; no CORS/trust policy inferred. | Direction-approved policy plus enforcement evidence. |
| F-003 | `OPEN` conditional | `EXTERNAL_EVIDENCE_REQUIRED` / owner decision for secret and settings semantics. | Storage, rotation, retention and authorization owner. |
| F-004 | `OPEN` route-specific hard | `TRUE_HARD_FRONTIER`; all 36 rows preserved as `UNKNOWN`. | Direction destination policy plus route compatibility evidence. |
| F-005 | `OPEN` conditional | Audit complete; positive route-to-canonical proof still absent. | Demonstrated adapter/coverage or an explicit containment decision. |
| F-006 | `OPEN` conditional | Lifecycle findings remain non-activating. | Full lifecycle call-chain contract and tests. |
| F-007 | `OPEN` external evidence | Provider/credential/network claim remains unproven. | Authorized provider and deployment evidence. |
| F-008 | `OPEN` conditional | Store ownership, retention and recovery remain gaps. | Named store owner and tested operational boundary. |
| F-009 | `DEFERRED` resolvable | Sandbox containment remains proven; product restore is not claimed. | Product restore evidence in a later authorized scope. |
| F-010 | `OPEN` conditional | Workforce readiness remains internal and inactive. | Activation, provider, approval and deployment gates. |
| F-011 | `OPEN` true hard | Closed for the 3.x phase exit by explicit Direction acceptance. | Future gates and P4 entry contract remain mandatory. |

## What is complete at this point

- Original 3.0–3.9 scope has one primary record per scope.
- Backend source truth, known call paths, contract surfaces and negative
  boundaries are cross-referenced to published evidence.
- The 36-route inventory is complete and independently reusable by the
  decision packet.
- Findings have an adopted Direction decision without claiming implementation.
- The P4 4.x entry contract is executable in shape, but no 4.x implementation is started.

## What remains explicitly open

- deployed ingress, identity, tenant and CORS policy;
- settings, secret lifecycle and persistence ownership;
- provider reachability, credentials, egress, cost and external traffic;
- route destination, compatibility and canonical adapter authority;
- product restore/recovery and active workforce activation;
- External evidence and future P4 entry gates; no 3.x Direction decision remains open.

`ROADMAP_3_X_ORIGINAL_SCOPE_EVIDENCE_COVERAGE_RECONSTRUCTED`
