# Roadmap 4.x Macro-Mission 04.1

## OCI necessary and sufficient inheritance

## Active contract

`NECESSARY_AND_SUFFICIENT_INHERITANCE`

This is the active future contract for Operational Capability Inheritance.
The superseded historical wording is preserved only where it belongs to closed
checkpoints or evidence; it is not rewritten in history and is not an active
contract here.

Necessary and sufficient does not mean inherit everything. It means provide
everything demonstrated as necessary and sufficient for the authorized task,
agent, model, domain and risk, while excluding irrelevant, incompatible,
unverified, private or unauthorized material. The inclusion and exclusion
reason for each element must remain traceable.

## Three bounded layers

1. `INITIAL_REQUIRED_INHERITANCE`: the validated base needed to begin the
   assigned mission.
2. `ON_DEMAND_AUTHORIZED_INHERITANCE`: additional capability admitted only
   after a demonstrated need and an explicit authorization decision.
3. `CONTINGENCY_AND_FALLBACK_INHERITANCE`: compatible recovery, fallback and
   escalation material required for the same authorized objective.

The base may grow when evidence demonstrates a new need. It may not grow from
performance claims, broad role names, subscription tier, empty identity,
wildcard capability, inherited tenant content or a query parameter.

## Active implementation boundary

The existing compiler remains deterministic and development-only. Its current
pack contract keeps runtime, execution and payload disabled and requires
explicit human approval. This mission documents the stronger inheritance
semantics without activating injection, providers, agents, runtime, production
stores or permissions.

## Selection record

A future compilation record must bind:

- mission and agent identity;
- task, domain and risk;
- primary and alternative model fit;
- required capabilities and evidence;
- included and excluded items with reasons;
- privacy and tenant scope;
- fallback and escalation;
- compatibility and freshness;
- reviewer and authorization;
- rollback and expiry conditions.

An OCI pack transfers structured capability, not weights, raw memory, private
reasoning, raw conversations, secrets or complete vault history. A conflict is
excluded and recorded under current-contract precedence. There is no silent
application and no automatic promotion.

## Historical preservation

Closed Macro 3.x, UI/UX and GOKV records are historical evidence. Their wording
and snapshots remain immutable. Only live references and future contracts use
`NECESSARY_AND_SUFFICIENT_INHERITANCE`. This distinction is enforced by the
Macro 04.1 tests rather than a global replacement.
