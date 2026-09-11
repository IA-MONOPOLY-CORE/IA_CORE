# GOKV OCI Resource Governance 0.4

`ROADMAP_3X_MACRO_02_OCI_RESOURCE_GOVERNANCE_MATERIALIZED`

This station makes relevance delivery explicit without widening the execution boundary. The existing compiler still selects only `PROMOTED` records by default, or `PROMOTED` plus `VALIDATED` in the explicitly requested `DEVELOPMENT_VALIDATED` mode. `CANDIDATE`, `OBSERVED`, `REVISED`, `DEPRECATED`, and `REPLACED` records remain excluded.

## Explicit budget

A development request may declare `resource_budget` with:

- `max_items`: maximum number of relevant records;
- `max_serialized_bytes`: maximum sum of deterministic serialized record sizes;
- `priority_knowledge_ids`: explicit deterministic preference order.

The compiler applies the budget after compatibility matching and before pack construction. The final IDs remain sorted for stable downstream inspection. When a relevant record cannot fit, `evidence_summary.omitted_relevant_items` records its ID and either `RESOURCE_BUDGET_MAX_ITEMS` or `RESOURCE_BUDGET_MAX_SERIALIZED_BYTES`. There is no silent truncation.

Without an explicit budget, all compatible records continue to be included, preserving the prior behavior and the existing pack IDs for historical requests.

## Boundary

This is a development-time contract and schema change only. It does not invoke models, read embeddings, call providers, connect to runtime or product code, create payloads, grant permissions, execute agents, or persist product state. A budget does not promote knowledge and does not make an omitted record applicable; it makes the omission auditable for the next governed mission.

## Verification

The focal contract test covers deterministic priority, item and byte budgets, explicit omission reasons, invalid budget rejection, and the unchanged disabled runtime contract.
