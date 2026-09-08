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
