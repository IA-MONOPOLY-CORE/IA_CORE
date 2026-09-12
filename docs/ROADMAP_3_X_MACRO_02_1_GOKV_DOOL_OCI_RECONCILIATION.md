# Roadmap 3.x Macro-Mission 02.1 GOKV, DOOL, and OCI Reconciliation

## Disposition

Macro 02's `NO_LEARNING_FOUND` conclusion is reopened only for the bounded
observations named by Macro 02.1. The conclusion is not rewritten in place.
Macro 02.1 records a new learning event and post-block loop with
`LEARNING_FOUND`, three new `CANDIDATE` items, and no automatic promotion.

## Reused knowledge

The following existing items were applied without duplication:

- `focal_group_canonical_deep_test_policy`: expanded the test depth decision to
  include pre-collection and import safety.
- `local_rollback`: used as recovery only; it does not excuse a write that was
  already made to a tracked path.
- `station_local_commits`: used for the new station sequence and explicit hash
  evidence.
- `real_diff_over_planned_commit_name`: used to evaluate the actual 20-commit
  history rather than trusting subjects or prior grouping.

## New candidates

- `test_collection_must_be_side_effect_free`: collection/import cannot initiate
  provider, runtime, credential, persistence, or network work.
- `test_writes_require_temporary_boundary`: test writes must be temporary or
  sandbox-injected before the write; restoring afterward is not hermetic proof.
- `commit_repair_needs_explicit_parity`: inherited repairs receive individual
  real-diff verdicts and are not silently relabeled as full stations.

All three candidates have `DEVELOPMENT_ORIGIN`, source evidence, scope, limits,
failure modes, recovery, and future validation criteria. Their lifecycle is
candidate-only until independent validation exists.

## OCI boundary

The existing OCI compiler remains unchanged by this station. This reconciliation
uses the already governed development-time registry and event schemas. No
runtime, provider, network, payload, or automatic promotion path is enabled.
