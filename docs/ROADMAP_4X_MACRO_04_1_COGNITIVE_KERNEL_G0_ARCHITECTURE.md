# Roadmap 4.x Macro-Mission 04.1

## Cognitive Kernel Generation Zero architecture

## Architectural decision

`IA_CORE_COGNITIVE_KERNEL` is a governed composition, not a fourth family:

```text
KERNEL = IDENTITY + CONTRACTS + TYPED_CONNECTIONS + GOVERNANCE + INHERITANCE + FEEDBACK
```

The current materialization is an inert, deterministic graph contract over the
existing GOKV foundation. A logical node is a record, contract or validator;
it is not a server, microservice, worker, deployment, process or runtime
capability.

## Horizontal families

| Family | Responsibility | Current integration |
| --- | --- | --- |
| `GOKV` | Knowledge, evidence, lifecycle, validation, contradiction, provenance and freshness | Existing `gokv/schema.py`, storage, registry and promotion boundaries |
| `DOOL` | Development-origin learning, Owner decisions, method improvement, failures, recovery and generation lineage | Existing GOKV `DEVELOPMENT_ORIGIN` plus the permanent lineage contract |
| `OCI` | Bounded inheritance compilation, task/model/domain/risk fit, contingencies and fallbacks | Existing development-time compiler and explicit human approval boundary |

The families are horizontal peers. The graph does not place one above another,
does not replace a family with the kernel, and does not infer authority from an
edge. Every edge has an origin, direction, type, status, evidence and limits.

## Identity and node contract

Each node has a stable `node_id`, family, generation, kind, lifecycle status,
scope, provenance, evidence references, compatibility, confidentiality class,
creation time, supersession references and inheritance disposition. IDs are
unique within the graph. G0 nodes require non-empty evidence. Future
generation placeholders require empty evidence and cannot be selected as
operational learning.

The machine-readable contract is
`ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json`; the inert
validator is `gokv/kernel.py`.

## Typed connections

The initial catalog is:

`derived_from`, `confirms`, `contradicts`, `limits`, `supersedes`,
`compatible_with`, `tested_by`, `inheritable_by`, `requires`, `improves`,
`degrades`.

The catalog is extensible, but an edge is never created without a fact that
supports it. Orphan endpoints, reflexive edges, unknown relation types and
cross-tenant constraints fail closed.

## Generations

| Generation | Meaning | Materialization in 04.1 |
| --- | --- | --- |
| `G0_DEVELOPMENT_ORIGIN` | Real learning from building IA_CORE and explicit Owner decisions | Inert nodes with repository evidence |
| `G1_BETA_OPERATIONAL_LEARNING` | Future controlled beta observations | Placeholder only; no evidence |
| `G2_FIELD_OPERATIONAL_LEARNING` | Future real field outcomes, costs, failures and specialties | Placeholder only; no evidence |
| `GN_CONTINUOUS_EVOLUTION` | Future continuous improvement of build, verification, recovery and transfer | Placeholder only; no evidence |

G0 is origin, not sunset. Field operation extends DOOL and does not replace
development origin. No generation is a claim of model training or autonomous
learning.

## Governance and feedback

The graph records provenance, lifecycle, compatibility, limits, contradiction
and evidence. Promotion remains the existing GOKV decision, never an automatic
graph side effect. Success and failure may become inheritable assets only after
distillation, validation, scope review, privacy filtering and explicit
selection. Feedback is a governed relation, not a live feedback loop.

## Runtime boundary

The graph validator requires runtime, provider calls, external calls,
permission grants, automatic promotion, tenant reads, raw secret reads, model
training and payload activation to remain false. It does not invoke agents,
select a provider, inject a prompt, read a tenant, write the vault or expose a
route.
