# Roadmap 3.x Macro-Mission 01 - B-3 Coverage Contract

Mission: `roadmap_3x_macro_01_security_legacy_canonical_alignment`

## B-3 result

`CONTROL_PLANE_COVERAGE_CONTRACT = PASS_EXPLICIT_CONTRACT_ONLY_UNALIGNED_LEGACY_SURFACE`

B-3 reconciles request, permission, confirmation, payload and lifecycle
contracts. It does not claim that a contract module is a route authority. The
route-specific disposition from B-2 remains the source of truth for every
legacy route.

## Expected versus actual postconditions

| Expected postcondition | Actual evidence | Result |
| --- | --- | --- |
| Every route has a destination | 36 routes have a destination; all are `UNKNOWN` under the completed quality gate | PASS |
| No contract is mistaken for route authority | Canonical contract modules are not imported as HTTP adapters by `api.py`; no canonical module registers an `app` route | PASS |
| Owners are explicit | Owner candidates are documented by coherent piece in the F-004 reconnaissance record | PASS |
| Payload authority is not inferred | No payload migration, API v2, wrapper or route contract rewrite was performed | PASS |
| High-risk bypasses remain visible | `/api/chat`, `/api/settings`, `/api/domains/create` and agent mutations retain explicit legacy/boundary findings | PASS |
| Canonical coverage improves through deterministic alignment | No safe semantic-equivalent adapter was demonstrated | NO_SAFE_ALIGNMENT; coverage remains unchanged |

## Canonical contract owner ledger

| Contract family | Owner artifacts | Route authority status |
| --- | --- | --- |
| Permission/capability | `core/agent_permission_contract.py`, `core/capability_policy_schema.py` | Contract-only; no legacy route adapter |
| Secrets/output/context | `core/secrets_policy.py`, `core/output_boundary.py`, `core/context_boundary.py` | Contract-only; B-1 raw `api_key` boundary remains green |
| Activation/readiness | `core/runtime_activation_gate.py`, `core/operational_readiness_gate.py` | Contract-only; no activation route |
| Internal UI contract | `core/backend_internal_ui_contract.py`, `core/backend_internal_ui_payloads.py` | Read-only contract; no public endpoint |
| Exposure/request validation | `core/backend_internal_exposure_registry.py`, `core/backend_internal_request_envelope.py` | Registry/validator only; no route dispatch |
| Dispatcher/confirmation/response | `core/backend_internal_dispatcher.py`, `core/backend_internal_confirmation_gate.py`, `core/backend_internal_response_adapter.py` | Contractual and gated; not connected to legacy routes |
| Attempt/execution/lifecycle | `core/attempt_factory.py`, `core/execution_contract.py`, `core/execution_lifecycle_contract.py` | Non-operational contract surface; not a legacy route owner |

## Route-to-contract provenance

Static AST/import inspection shows that `api.py` directly imports catalog,
domain, supervisor/orchestration and model-recommendation helpers. It does not
import the internal backend request envelope, dispatcher, confirmation gate,
response adapter, permission contract or activation gate as an HTTP adapter.
Canonical internal modules contain no FastAPI route registration.

This is a negative coverage result, not a defect to repair inside this mission:
connecting a legacy route would require an explicit payload, owner,
authorization and compatibility decision. The B-2 destinations therefore stay
`UNKNOWN` and the coverage counts remain:

| Classification | Before | After B-3 |
| --- | ---: | ---: |
| `CANONICAL_CONTROL_PLANE_COVERED` | 0 | 0 |
| `PARTIALLY_COVERED` | 1 | 1 |
| `LEGACY_BYPASS_DEMONSTRATED` | 2 | 2 |
| `COVERAGE_NOT_DEMONSTRATED` | 33 | 33 |
| `NOT_APPLICABLE` | 0 | 0 |

## High-risk negative checks

| Surface | Finding |
| --- | --- |
| `POST /api/chat` | Directly calls `Supervisor.orchestrate_async`; no canonical permission/request-envelope/dispatcher path is demonstrated. No provider or agent was invoked during the audit. |
| `POST /api/settings` | Raw `api_key` input is rejected before persistence; no canonical settings owner or route authorization is demonstrated. |
| `POST /api/domains/create` | Existing domain primitive is documented as safe only under isolated/internal materialization boundaries; no public canonical materializer is enabled. |
| Agent mutation routes | Agent/paper schemas and permission contracts exist, but no canonical lifecycle adapter or confirmation route is demonstrated. |
| All mutative routes | No new confirmation, payload, runtime or execution semantics were introduced. |

## B-3 frontier result

`F-005` is resolved as a static provenance finding: canonical contracts exist,
but no route adapter is present. No new route-specific true-hard frontier was
discovered. F-006 (activation/provider), F-007 (external/provider evidence),
F-008 (persistence ownership) and workforce/persistence follow-on work remain
outside this mission and outside the authorized B-1 -> B-2 -> B-3 path.

This mission does not enter B-4, B-5, B-6 or B-7. The next candidate is a
separately scoped 3.x phase selected from the existing roadmap graph, not
compiled or executed here.

## Materiality and learning

- Product/API changes in B-3: none.
- Documentation/test changes: this record and the static B-3 guards.
- Runtime/provider/network/agent execution: none.
- Secrets read or printed: none.
- Learning reused: `DERIVE_SERVICE_OWNER_BEFORE_DESTINATION`,
  `CALLABLE_CHAIN_IS_NOT_AUTHORIZED_ROUTE`,
  `CONTRACT_EXISTS_IS_NOT_ROUTE_ADAPTER` and checkpoint-bounded historical
  guards.
- Learning state: `OBSERVED`; no automatic promotion.
