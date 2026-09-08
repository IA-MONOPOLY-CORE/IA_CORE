# GOKV 0.2 — DOOL and OCI Architecture

## Gate

`N1_GOKV_DOOL_OCI_ARCHITECTURE_PASSED`

## Post-Bootstrap Audit

GOKV 0.1 is solid in the following areas:

- a Git-backed canonical vault exists under `knowledge/global_operational/`;
- knowledge items have explicit schema, lifecycle, evidence, scope, and privacy fields;
- append-only learning events and execution metrics exist;
- Generation 0 contains 23 traceable records;
- the deterministic compiler defaults to `PROMOTED_ONLY`;
- a development-only CLI, protocol, and checkpoint exist;
- no product or runtime path consumes the vault.

The following items were deliberately incomplete:

- knowledge had no explicit origin taxonomy;
- lineage could not represent future field confirmation, refinement, limitation, contradiction, or supersession;
- no objective promotion assessment existed;
- compilation produced a pack but did not define authority precedence or conflict recording;
- no shadow evaluation measured what a pack was useful, irrelevant, or conflicting for;
- post-block capture did not yet formalize the handoff from one mission to the next.

## What `PROMOTED = 0` Means

`PROMOTED = 0` is the correct conservative result. It means no Generation 0 item has yet met a separately governed promotion threshold. It does not mean that the 16 `VALIDATED` items are unusable. They are available in explicit `DEVELOPMENT_VALIDATED` mode for development inspection and controlled inheritance.

Automatically promoting all 16 validated items would erase the distinction between evidence-backed validation and institutional reuse. It could make a narrow UI/build pattern appear globally authoritative, hide missing repetition or freshness evidence, and let an item outrank the current contract. GOKV 0.2 therefore adds assessment and inheritance boundaries without changing lifecycle status.

## DOOL

**Development-Origin Operational Learning** (`DOOL`) is operational knowledge acquired, observed, tested, refined, and structured while IA_CORE is being built, before the first external business operation. Generation 0 is the first DOOL expression.

DOOL records the gestation phase. It is not runtime learning, model training, copied private reasoning, copied conversations, or a claim that every construction pattern is field-proven.

The minimum origin taxonomy is:

- `DEVELOPMENT_ORIGIN`
- `FIELD_OPERATION`
- `MIXED_ORIGIN`
- `EXTERNAL_REFERENCE`
- `UNKNOWN`

`FIELD_OPERATION` is representable but not implemented in 0.2.

## OCI

**Operational Capability Inheritance** (`OCI`) is the controlled selection and compilation of relevant operational knowledge for a future development mission. OCI transfers structured capability, not weights, memory, private reasoning, or complete history.

The flow is:

```text
prior reasoning
  -> operational knowledge
  -> explicit selection
  -> deterministic compilation
  -> bounded capability pack
  -> development mission inspection
```

The first implementation is `DEVELOPMENT_TIME_OCI_V1`. It is explicit, development-only, and does not connect agents to runtime GOKV.

## Gestation and Field Operation

The ecosystem has two conceptual phases:

| Phase | Primary origin | Output | 0.2 status |
|---|---|---|---|
| `GESTATION_PHASE` | `DEVELOPMENT_ORIGIN` | DOOL | active and trackable |
| `FIELD_OPERATION_PHASE` | `FIELD_OPERATION` | field operational learning | representable, not implemented |

Knowledge is not deleted when the phase changes. Future field evidence may `CONFIRM`, `REFINE`, `LIMIT`, `CONTRADICT`, or `SUPERSEDE` a development-origin item. Those are representable lineage relations, not automatic decisions.

## Construction Accumulation Principle

`EACH_STAGE_BUILDS_THE_SYSTEM_AND_INCREASES_THE_CAPABILITY_OF_THE_NEXT`

Each stage should be able to leave:

```text
result + evidence + learning event + optional candidate
  -> GOKV
  -> execution pack
  -> better-prepared next stage
```

The loop is opportunistic, not compulsory. `NO_LEARNING_FOUND` is a valid outcome, and a stage must not invent knowledge merely to satisfy the loop.

## Minimal Changes Required

DOOL requires origin metadata and append-only operator supplements. OCI requires explicit development mode, authority precedence, conflict records, consumption/shadow evaluation, and a compact reusable post-block protocol. None requires runtime integration, field operation, model invocation, embeddings, UI changes, or autonomous promotion.

## Non-Goals

GOKV 0.2 does not implement runtime learning, productive agents, execution runtime, model calls, fine-tuning, embeddings, vector databases, RAG, downloads, external network, multi-business sharing, UI/backend/payload changes, providers, integrations, queues, schedulers, workers, or UI/UX 1.200 execution.
