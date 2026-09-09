# IA_CORE - Agent Workforce Readiness Architecture

## Gate

`ROADMAP_3_0_A_N2_AGENT_WORKFORCE_REQUIREMENTS_PASSED`

## Agent Blueprint Library

IA_CORE should maintain an `AGENT_BLUEPRINT_LIBRARY`, not an army of idle
agents. A blueprint is reusable professional DNA from which the required agent
can be materialized later for a business, team or task. The blueprint is not a
running agent, provider session, paper file, memory database or permission grant.

The future composition chain is:

`BUSINESS_REQUIREMENTS -> REQUIRED_CAPABILITIES -> REQUIRED_ROLES ->
AGENT_BLUEPRINTS -> MODEL/HARDWARE_POLICY -> MEMORY_NAMESPACES -> PRESETS ->
PAPERS -> AGENTS -> TEAMS -> ORGANIZATION`.

## Conceptual AGENT_READY_V1 contract

`AGENT_READY_V1` is a future readiness contract, not a product schema in this
mission. An agent is not `READY_TO_CONSTITUTE_BUSINESS` because a JSON/config or
preset exists.

### Identity

- `professional_profile_id`
- `role_id`
- `specialization_id`
- `archetype`
- `seniority`
- `purpose`

### Capability

- capabilities;
- responsibilities;
- limitations;
- input contract;
- output contract;
- stop conditions;
- escalation policy;
- success criteria.

### Knowledge and provenance

- paper seed;
- professional knowledge scope;
- domain context policy;
- knowledge update policy;
- provenance.

### Memory

- memory policy;
- logical agent namespace;
- team namespace policy;
- business namespace policy;
- access permissions;
- retention, isolation, provenance, deletion and supersession rules.

### Model and capacity

- workload;
- reasoning need;
- model policy;
- provider policy;
- local/cloud/hybrid preference;
- hardware requirements;
- fallback and escalation policy;
- concurrency assumptions.

### Operation and organization

- preset;
- allowed and blocked tools/capabilities;
- permission contract;
- confirmation requirements;
- audit/evidence contract;
- lifecycle state;
- compatible team types;
- supervisor/subordinate compatibility;
- areas, niches, business types and scale compatibility;
- hierarchy compatibility.

## Logical memory ownership

The preferred future architecture is shared memory infrastructure with logically
isolated namespaces or collections:

`GLOBAL/INSTITUTIONAL -> BUSINESS_ID -> BUSINESS_MEMORY -> TEAM_ID ->
TEAM_MEMORY -> AGENT_ID -> AGENT_MEMORY`.

Logical ownership means explicit sharing, retrieval permissions, retention,
deletion, supersession, provenance and audit. It does **not** require one
physical vector database per agent. Vector storage, runtime persistence and
memory execution remain future implementation work.

## Current versus future

Current profiles, roles, specializations, model policies, permission contracts,
agent config metadata, paper schemas and sandbox materializers are reusable
inputs or partial contracts. Future `AGENT_READY_V1`, blueprint completeness,
logical namespace enforcement, team compatibility and readiness scoring are not
implemented by Roadmap 3.0.A.

