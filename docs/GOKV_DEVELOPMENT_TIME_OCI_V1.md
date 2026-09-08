# GOKV 0.2 — Development-Time Operational Capability Inheritance

## Gate

`N5_GOKV_DEVELOPMENT_TIME_OCI_PASSED`

`DEVELOPMENT_TIME_OCI_V1` compiles an explicit `DEVELOPMENT_VALIDATED` request into an inspectable operational guidance pack. It is a development helper, not runtime learning and not a productive agent integration.

## Authority Precedence

The pack records this order:

1. `SECURITY_PRIVACY_HARD_CONTRACTS`
2. `CURRENT_MISSION_EXPLICIT_CONSTRAINTS`
3. `CURRENT_CANONICAL_ARCHITECTURE`
4. `CURRENT_REPOSITORY_STATE`
5. `GOKV_OPERATIONAL_GUIDANCE`

GOKV guidance can inform a mission but can never override the current contract, explicit mission restrictions, canonical architecture, or actual repository state.

## Conflict Policy

`CURRENT_CONTRACT_WINS` is mandatory. A conflict excludes the knowledge from application and can be recorded as `gokv.knowledge_conflict_event.v1`. Resolution is not inferred, and no knowledge is applied silently.

## Consumption Result

The development-only consumption record distinguishes available, selected, applied, unused, irrelevant, conflicted, helpful, new candidates, operator interventions, and clarification requests. It also records pack bytes and item count. A result such as `INSPECTION_ONLY` is valid when no productive agent has applied the pack.

## Capability Boundary

OCI does not copy weights, conversations, private reasoning, or complete history. It supplies the minimum relevant structured guidance requested by the mission. No model invocation, runtime consumer, tool execution, endpoint, scheduler, queue, provider, integration, or UI change is introduced.
