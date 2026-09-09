# Roadmap 3.2 - Legacy API <-> Canonical Control Plane Coverage Audit

## Mission

`MISSION_ID`: `roadmap_3_2_legacy_api_canonical_control_plane_coverage_read_only_audit`

`MODE`: `READ_ONLY_PRODUCT_AUDIT`

`BASELINE`: `2255295f5ffe4f7348476acfca606a84aa12af35`

This audit answers two questions without implementing a bridge or a fix:

1. What is the real relationship between the 36 legacy routes and the current
   canonical control plane?
2. Which future remediation semantics are derivable from existing contracts,
   and which are true hard frontiers?

Method: static repository inspection, AST route census, source call-path
analysis, current contract/docs/test provenance and GOKV/OCI manifest reading.
The application was not imported or started. No provider, network, runtime,
agent, endpoint, store or secret value was accessed.

`IA_CORE_clean(1).zip` was treated only as a historical, non-authoritative
snapshot and was not opened or used.

## Initial State and Authority

| Item | Result |
| --- | --- |
| Repository | `C:/IA_CORE` |
| Branch | `main` |
| HEAD | `2255295f5ffe4f7348476acfca606a84aa12af35` |
| `origin/main` local | `2255295f5ffe4f7348476acfca606a84aa12af35` |
| Ahead/behind | `0/0` |
| Working tree | clean |
| `git diff --check` | PASS |
| Historical zip | not opened; non-authoritative by contract |
| Product mutation | forbidden and not performed |
| Runtime/provider/network | forbidden and not performed |
| Secret values | not read, printed or copied |

Authority precedence used:

1. Security/privacy hard contracts.
2. Current mission constraints.
3. Current canonical architecture.
4. Current repository state and Git.
5. GOKV operational guidance.

GOKV/DOOL/OCI state is `PROMOTED_ONLY`, `CURRENT_CONTRACT_WINS`, minimum
sufficient inheritance, with `conditioned_autonomy=VALIDATED` and not promoted.
No new learning was promoted or appended.

## Station Graph

| Station | Result | Diff |
| --- | --- | --- |
| N0 Preflight and authority reconstruction | PASS | NO_DIFF |
| N1 Canonical control-plane census | PASS | documented |
| N2 36-route coverage matrix | PASS | documented |
| N3 Contract/payload/permission reconciliation | PASS | documented |
| N4 High-risk route reconciliation | PASS | documented |
| N5 Remediation-readiness classification | PASS | documented |
| N6 Cross-layer synthesis | PASS | documented |
| N7 Tests/checkpoint/publication | completed after validation | documented |

## Canonical Control-Plane Census

The canonical plane exists as a set of contract-only validators, safe internal
services and controlled sandbox implementations. Its existence is not evidence
that a legacy route invokes it.

| ID | Control | State | Source | Route connection |
| --- | --- | --- | --- | --- |
| C-001 | Agent permission contract | CANONICAL_CONTRACT_ONLY | `core/agent_permission_contract.py` | none demonstrated |
| C-002 | Capability policy | CANONICAL_CONTRACT_ONLY | `core/capability_policy_schema.py` | none demonstrated |
| C-003 | Secrets policy | CANONICAL_CONTRACT_ONLY | `core/secrets_policy.py` | none demonstrated |
| C-004 | Context/model/output boundaries | CANONICAL_CONTRACT_ONLY | `core/context_boundary.py`, `core/model_invocation_boundary.py`, `core/output_boundary.py` | none demonstrated |
| C-005 | Runtime activation gate | CANONICAL_CONTRACT_ONLY | `core/runtime_activation_gate.py` | none demonstrated |
| C-006 | Operational readiness gate | CANONICAL_CONTRACT_ONLY | `core/operational_readiness_gate.py` | none demonstrated |
| C-007 | Attempt factory | CANONICAL_CONTRACT_ONLY | `core/attempt_factory.py` | none demonstrated |
| C-008 | Execution/lifecycle contracts | CANONICAL_CONTRACT_ONLY | `core/execution_contract.py`, `core/execution_lifecycle_contract.py`, `core/lifecycle_writer.py` | none demonstrated |
| C-009 | Active contract | CANONICAL_CONTRACT_ONLY | `core/active_contract.py` | none demonstrated |
| C-010 | Active executor | CURRENT_IMPLEMENTATION_CALLABLE_BUT_GATED | `core/active_executor.py` | no API registration |
| C-011 | Internal UI contract | CURRENT_IMPLEMENTATION_READ_ONLY_CONTRACT | `core/backend_internal_ui_contract.py` | none demonstrated |
| C-012 | Exposure registry | CURRENT_IMPLEMENTATION_READ_ONLY_CONTRACT | `core/backend_internal_exposure_registry.py` | none demonstrated |
| C-013 | Request envelope | CURRENT_IMPLEMENTATION_READ_ONLY_VALIDATOR | `core/backend_internal_request_envelope.py` | none demonstrated |
| C-014 | Internal dispatcher | CURRENT_IMPLEMENTATION_CONTRACTUAL_NO_RUNTIME | `core/backend_internal_dispatcher.py` | none demonstrated |
| C-015 | Confirmation gate | CURRENT_IMPLEMENTATION_READ_ONLY_VALIDATOR | `core/backend_internal_confirmation_gate.py` | none demonstrated |
| C-016 | Response adapter | CURRENT_IMPLEMENTATION_READ_ONLY_ADAPTER | `core/backend_internal_response_adapter.py` | none demonstrated |
| C-017 | Stable UI payloads | CURRENT_IMPLEMENTATION_READ_ONLY_PAYLOAD | `core/backend_internal_ui_payloads.py` | none demonstrated |
| C-018 | Sandbox validation/materialization | CURRENT_IMPLEMENTATION_CONTROLLED_SANDBOX | `core/backend_internal_validate_domain_service.py`, `core/domain_materializer.py` | legacy domain route only uses local path |
| C-019 | Audit/observability | CURRENT_IMPLEMENTATION_NOT_LEGACY_CONNECTED | `core/audit_store.py`, `core/observability.py` | none demonstrated |
| C-020 | Approval workflow | CANONICAL_CONTRACT_ONLY | `core/approval_workflow.py` | none demonstrated |

Provenance and test evidence for every row are in the JSON evidence artifact.

### Canonical Semantics

The existing contracts establish, among other things:

- default deny for undeclared or dangerous capabilities;
- no runtime, execution, provider, tool, network, secret or operational-domain
  activation from contract-only modules;
- safe request envelopes that reject public/external/runtime callers, secret-like
  fields and operational flags;
- confirmation requirements for controlled-write/lifecycle services;
- stable JSON-safe internal payloads with backend-owned readiness and actions;
- sandbox-root and operational-path rejection for controlled materialization.

None of these findings authorizes a legacy bridge, auth policy, CORS policy or
runtime activation. Those decisions remain outside this mission.

## Coverage Matrix: All 36 Routes

`contract_exists_for_relevant_surface` means a related canonical contract is
present. `route_uses_contract` is true only with a positive source call path to
the canonical entrypoint. The latter is false for all 36 routes in this audit.
This distinction is intentional: `CONTRACT_EXISTS` is not
`ROUTE_USES_CONTRACT`.

| Path | Method | Registration | Primary coverage | Contract exists | Route uses contract |
| --- | --- | ---: | --- | --- | --- |
| `/api/status` | GET | 505 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/memory` | GET | 577 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/logs` | GET | 611 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/metrics/dynamic` | GET | 628 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/debate/start` | POST | 677 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/validation/start` | POST | 708 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/validation/next` | GET | 764 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/validation/{validation_id}` | GET | 798 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/validation/{validation_id}/reveal` | POST | 806 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/ranking` | GET | 822 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/evolucion/stats` | GET | 830 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/evolucion/reset` | POST | 843 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/debate/{debate_id}` | GET | 854 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/debates` | GET | 862 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/chat` | POST | 872 | LEGACY_BYPASS_DEMONSTRATED | yes | no |
| `/api/learn` | POST | 948 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/conversation/{conversation_id}` | GET | 971 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/catalogs/domain-creation` | GET | 985 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/catalogs/roles` | GET | 994 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/catalogs/specializations` | GET | 1003 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/domains/list` | GET | 1016 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/domains/{domain_id}/profile-catalog` | GET | 1027 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/domains/{domain_id}/agent-presets` | GET | 1040 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/domains/{domain_id}/agent-presets/match` | GET | 1059 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/domains/create` | POST | 1096 | PARTIALLY_COVERED | yes | no |
| `/api/agents/create` | POST | 1180 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/settings` | POST | 1449 | LEGACY_BYPASS_DEMONSTRATED | yes | no |
| `/api/settings` | GET | 1505 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/agents/model-recommendation` | POST | 1526 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/system/hardware-profile` | GET | 1603 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/system/model-compatibility` | POST | 1628 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/agents/list` | GET | 1647 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/agents/{agent_id}` | PUT | 1720 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/agents/{agent_id}` | DELETE | 1802 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/api/agents/{agent_id}/regenerate-paper` | POST | 1836 | COVERAGE_NOT_DEMONSTRATED | yes | no |
| `/` | GET | 1934 | COVERAGE_NOT_DEMONSTRATED | yes | no |

### Coverage Counts

| Classification | Count | Meaning |
| --- | ---: | --- |
| CANONICAL_CONTROL_PLANE_COVERED | 0 | no legacy route was proven to traverse a canonical entrypoint |
| PARTIALLY_COVERED | 1 | local domain validation exists, but canonical request/permission/confirmation/runtime coverage does not |
| LEGACY_BYPASS_DEMONSTRATED | 2 | positive legacy call-path evidence exists for `/api/chat` and POST `/api/settings` |
| COVERAGE_NOT_DEMONSTRATED | 33 | evidence is insufficient to claim either canonical coverage or bypass |
| NOT_APPLICABLE | 0 | every route remains an API exposure for which boundary relevance cannot be dismissed |

## High-Risk Reconciliation

### `POST /api/chat`

The source call path is `api.py:873` -> `Supervisor.orchestrate_async` ->
`AgentManager` -> `ProviderRegistry` -> provider adapters. `api.py` contains no
demonstrated call to the permission contract, secret policy, runtime activation
gate, request envelope, dispatcher or confirmation gate. This is a positive
legacy call path, so the primary classification is
`LEGACY_BYPASS_DEMONSTRATED`, not merely "unknown". Actual invocation,
credential state, network and deployment remain untested and unknown.

### `POST /api/settings`

The handler accepts the `api_key` field by form, constructs a settings mapping,
writes `memory/user_settings.json`, and conditionally rewrites `config.py` when
the field is supplied (`api.py:1449-1492`). The response also returns the
settings object. The canonical secret policy exists but is not on this route's
call path. Secret values were not read or included in evidence.

### The 14 mutative routes

The exact 14 are:

`/api/debate/start`, `/api/validation/start`,
`/api/validation/{validation_id}/reveal`, `/api/evolucion/reset`, `/api/chat`,
`/api/learn`, `/api/domains/create`, `/api/agents/create`, `/api/settings`,
`/api/agents/model-recommendation`, `/api/system/model-compatibility`,
`PUT /api/agents/{agent_id}`, `DELETE /api/agents/{agent_id}` and
`/api/agents/{agent_id}/regenerate-paper`.

They have handler-local validation and/or source write candidates, but no
demonstrated canonical request envelope, route authorization, confirmation or
runtime gate. That is not a claim that every route is deployed or invoked.

## Permission, Request, Confirmation and Lifecycle Relationship

| Layer | Canonical state | Legacy API relationship |
| --- | --- | --- |
| Identity/authentication | no route-local identity dependency demonstrated | coverage not demonstrated; deployment edge unknown |
| Authorization/ownership | permission/capability contracts exist; HTTP owner/tenant semantics are not connected | coverage not demonstrated |
| Request envelope | internal envelope rejects untrusted caller kinds and unsafe fields | no legacy route entrypoint demonstrated |
| Stable payload | internal payloads/adapter normalize backend decisions | legacy routes return legacy dicts/projections |
| Confirmation | internal gate validates explicit human confirmation for controlled services | no legacy route gate call demonstrated |
| Activation/runtime | dedicated gate is disabled/contract-only | no global coverage over legacy API demonstrated |
| Executor | active executor is gated and not API-registered | no legacy route call path demonstrated |
| Provider/network | real legacy adapters are source-callable | no provider/network invocation was performed |
| Writes/stores | sandbox controls exist; legacy writes also exist | route-level canonical store guard not demonstrated |
| Audit/evidence | append-only audit implementation exists | route-level canonical audit path not demonstrated |

## Reconciliation of the 7 Roadmap 3.1 Findings

All seven IDs and severities are preserved. No severity was changed.

| Finding | Coverage result | Remediation readiness |
| --- | --- | --- |
| F-3.1-001 route auth/authz not demonstrated | preserved; all 36 routes | MORE_READ_ONLY_TRUTH_REQUIRED |
| F-3.1-002 wildcard CORS | source-confirmed legacy/global setting | REQUIRES_DIRECTION_POLICY_DECISION |
| F-3.1-003 settings secret/write path | legacy bypass demonstrated | REMEDIATION_SEMANTICS_DERIVABLE_FROM_EXISTING_CONTRACT, with auth/storage dependencies |
| F-3.1-004 chat provider-capable path | legacy bypass demonstrated | MORE_READ_ONLY_TRUTH_REQUIRED |
| F-3.1-005 mutation routes without route authz | 14-route coverage gap preserved | REQUIRES_DIRECTION_POLICY_DECISION |
| F-3.1-006 gates not proven global over legacy API | legacy coverage gap is now call-path reconciled | REQUIRES_DIRECTION_POLICY_DECISION |
| F-3.1-007 provider/network reachability | not exercised | REQUIRES_RUNTIME_EVIDENCE |

## Remediation Readiness and Frontiers

### Semantics derivable from existing contracts

- Secret candidate classification/redaction/blocking rules.
- Deny-by-default runtime, execution, tool, model, network, integration and
  operational-domain semantics.
- Internal request safety, confirmation requirements and stable payload rules.
- Sandbox-only path and operational-root rejection for the canonical sandbox flow.

No fix, bridge or policy was written.

### Apparent frontiers

- The canonical safety semantics themselves are not a frontier: they are
  explicit and tested in their own modules.
- The internal request/confirmation/payload chain is also explicit for the
  internal surface.
- Sandbox controlled-write semantics are explicit for the sandbox surface.

### True hard frontiers

- Identity, tenant/business/team/agent ownership semantics for legacy HTTP
  callers.
- Whether legacy API is bridged, retired, separately governed or retained.
- Human policy for allowed CORS origins/methods/headers.
- External deployment edge, TLS, WAF and ingress controls.
- Runtime/provider/network evidence, which is outside this read-only mission.

## Tests and Gates

The Roadmap 3.2 guard verifies:

- mission id, baseline and exact 36-route AST census;
- 22 GET, 12 POST, 1 PUT, 1 DELETE and 14 mutative routes;
- all coverage fields and classification counts;
- deep analysis for `/api/chat` and `/api/settings`;
- canonical census presence, provenance and test evidence;
- distinction between contract existence and route usage;
- all seven Roadmap 3.1 findings and readiness classifications;
- no unsupported deployment claim, secret value or remediation code;
- narrative/JSON consistency and authorized diff scope.

Focal policy:

```text
python -m json.tool docs/ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_EVIDENCE.json
python -m pytest -q tests/test_roadmap_3_2_legacy_api_canonical_control_plane_audit.py
python -m pytest -q tests/test_roadmap_3_1_security_permission_activation_boundary_audit.py
git diff --check
```

Safe related contract tests were inspected by name before selection. No network,
provider, runtime, productive-write or secret-access suite was executed.

The Roadmap 3.1 historical guard was executed unchanged in a detached worktree
at its published checkpoint (`2255295f5ffe4f7348476acfca606a84aa12af35`) and
passed (`10 passed`). Running that closed-world 3.1 guard against the current
3.2 tree rejects the four legitimate 3.2 artifacts by design; that historical
test was not modified or relaxed.

## Scope and Side-Effect Closure

Modified artifacts are limited to the four Roadmap 3.2 files authorized by the
mission. `api.py`, `core/`, `agents/`, `providers/`, `domains/`, `config.py`,
contracts, schemas, payloads, UI, stores, memory, knowledge/GOKV and deployment
files remain unmodified. No product code, remediation, bridge, auth/authz,
CORS policy, provider, runtime, execution, endpoint or integration change was
made.

## Result

`ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_COVERAGE_READ_ONLY_AUDIT_PASSED`

Publication is permitted only after the focal/historical tests, diff gate and
final Git remote verification pass. The next roadmap must not be selected here;
this report is the handoff to the CHAT / ARCHITECT for post-mission
architectural recalculation.
