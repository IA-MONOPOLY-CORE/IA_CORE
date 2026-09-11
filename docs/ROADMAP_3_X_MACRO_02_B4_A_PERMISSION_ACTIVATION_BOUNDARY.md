# Roadmap 3.x Macro-Mission 02: B4-A Permission Activation Lifecycle Boundary

`ROADMAP_3X_MACRO_02_B4_A_PERMISSION_ACTIVATION_BOUNDARY_MATERIALIZED`

## Static chain

This station consolidates the repository evidence for a future permission and
activation chain. It does not claim that the chain is connected to an HTTP
route, product runtime, provider, agent, or operational executor.

| Stage | Contract surface | Current evidence | Boundary result |
| --- | --- | --- | --- |
| contract | `core/agent_permission_contract.py` | permission records and validators exist | contract-only |
| capability | `core/capability_policy_schema.py` | capability policy schema and blocked flags exist | contract-only |
| request | `core/backend_internal_request_envelope.py` | internal envelope validation exists | internal contract-only |
| dispatcher | `core/backend_internal_dispatcher.py` | dispatcher validates internal requests and blocks missing confirmation | no route adapter proven |
| confirmation | `core/backend_internal_confirmation_gate.py` | confirmation scope and controlled-service requirements exist | no autonomous approval |
| activation | `core/runtime_activation_gate.py` | activation signals are classified and blocked before runtime | runtime disabled |
| readiness | `core/operational_readiness_gate.py` | readiness is declarative and fail-closed | not runtime-ready |
| execution/lifecycle | `core/execution_contract.py`, `core/execution_lifecycle_contract.py` | future execution and lifecycle states are validated with disabled flags | no execution |
| legacy callers | `api.py`, Macro 01 route evidence | 36 legacy routes remain unaligned or not demonstrated | route coverage unresolved |

## Required proof order

Future route work must prove the chain in order. A callable symbol is not
permission, an internal dispatcher is not an HTTP adapter, readiness is not
activation, and a lifecycle schema is not execution. A missing link remains an
explicit frontier rather than being inferred from neighboring contracts.

In short: **a callable symbol is not permission**, and **readiness is not
activation**.

## Safety contract

- `runtime_enabled`, `execution_enabled`, tool execution, and product mutation remain disabled.
- No endpoint, integration, provider, network, secret, payload, UI, or legacy route was changed.
- No permission is granted by this document.
- No route is reclassified as covered by contract presence alone.

## Evidence and next producer

The current station proves contract availability and fail-closed boundaries.
The next evidence producer for route coverage is a separately authorized,
read-only source trace that demonstrates a specific legacy caller to a specific
canonical entrypoint. External identity, tenant, deployment, and traffic
evidence remain outside this station.
