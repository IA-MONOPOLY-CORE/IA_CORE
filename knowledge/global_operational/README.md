# GOKV 0.1 - Global Operational Knowledge Vault

This is a development-time, Git-backed knowledge foundation for IA_CORE.

- `schema/` contains machine-readable contracts.
- `items/` contains append-only versioned knowledge items.
- `events/` will contain learning events, never automatic promotion.
- `metrics/` will contain execution metrics with explicit measurement quality.
- `packs/` will contain deterministic development-only execution packs.
- `registry.json` is a derived index rebuilt by the GOKV helper.

The vault does not activate runtime, agents, models, network, tools, APIs,
embeddings, vector databases, RAG or integrations.

## GOKV 0.2

- DOOL is represented by `learning_origin`; Generation 0 normalizes to `DEVELOPMENT_ORIGIN` without rewriting item files.
- Lineage can represent `CONFIRM`, `REFINE`, `LIMIT`, `CONTRADICT`, and `SUPERSEDE` without automatic resolution.
- Operator measurements are append-only supplements; promotion assessment is non-automatic.
- `DEVELOPMENT_TIME_OCI_V1` and shadow evaluation are development-only.
- Reusable loop blocks: `GOKV_POST_BLOCK_CAPTURE_V1` and `GOKV_PRE_MISSION_INHERITANCE_V1`.
- UI/UX 1.200 has a shadow pack only and remains unexecuted.
