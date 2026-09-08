# GOKV 0.2 — Provenance and Lineage Contract

## Gate

`N2_GOKV_PROVENANCE_AND_LINEAGE_PASSED`

## Compatibility Decision

GOKV 0.2 extends `gokv.knowledge_item.v1` compatibly. Existing item files are not rewritten. The validator supplies defaults when legacy files omit the optional fields:

- `learning_origin`: `DEVELOPMENT_ORIGIN`;
- `lineage`: `[]`.

The derived registry records the normalized origin. New items created through `build_knowledge_item` persist both fields. This is a compatibility normalization plus derived metadata, not a silent historical rewrite or version erasure.

## Origin Taxonomy

| Origin | Meaning |
|---|---|
| `DEVELOPMENT_ORIGIN` | Learned during IA_CORE construction. |
| `FIELD_OPERATION` | Learned during future real business operation; not implemented in 0.2. |
| `MIXED_ORIGIN` | Explicitly combines development and field evidence. |
| `EXTERNAL_REFERENCE` | Imported reference evidence, not IA_CORE experience. |
| `UNKNOWN` | Origin not established. |

All 23 Generation 0 records normalize to `DEVELOPMENT_ORIGIN`.

## Lineage

Lineage entries are declarative records with a related knowledge ID, related origin, evidence references, notes, and one relation:

`CONFIRM`, `REFINE`, `LIMIT`, `CONTRADICT`, or `SUPERSEDE`.

The contract represents possible future relationships. It does not automatically change status, confidence, version, applicability, or promotion. A future field item can therefore challenge DOOL without overwriting it.

## Boundary

No field operation, automatic conflict resolution, autonomous promotion, runtime retrieval, agent consumption, or product integration is implemented by this contract.
