# GOKV 0.3 - First Institutional Promotion Report

## Executive result

`IA_CORE_GOKV_FIRST_INSTITUTIONAL_PROMOTION_0_3_PASSED`.

The first institutional promotion was executed through the reusable
`promote-authorized` transaction. Exactly seven explicitly authorized
`VALIDATED` items became `PROMOTED`. No other item was promoted. The
assessment used for the decision remains immutable and still records no
automatic promotion; the post-promotion governance check was recomputed over
the remaining nine `VALIDATED` items.

## N0 and N1

N0 passed as `N0_GOKV_FIRST_INSTITUTIONAL_PROMOTION_GATE_PASSED`: the seven
authorized IDs matched the seven `PROMOTION_READY` IDs, with zero unknown,
not-ready, unowned-ready, conflicting, or missing-evidence cases.

N1 is persisted at
`knowledge/global_operational/authorizations/first_institutional_promotion_authorization_0_3.json`.
It is machine-readable, Direction-bound, non-wildcard, checkpoint-scoped and
sets `automatic_promotion = false`. `conditioned_autonomy` is explicitly
deferred with `DIRECTION_APPROVAL_REQUIRED`, `KEEP_VALIDATED` and
`MORE_EVIDENCE_REQUIRED`.

## N2 mechanism and historical preservation

The reusable mechanism is `gokv.institutional_promotion.promote_authorized_items`
and the CLI entry point is:

```text
python -m gokv promote-authorized <authorization.json> <assessment.json>
```

It validates the exact authorization, current lifecycle, readiness category,
effective evidence including the recorded independent overlay, assessment
freshness, scope, provenance, privacy, lineage and reversible field
preservation before writing. It rejects wildcard/unauthorized IDs, candidates,
duplicate or stale transitions, insufficient evidence, scope widening and
provenance mutation. Item writes, registry rebuild and promotion audit event
are guarded by a rollback path for transaction failures.

No history was rewritten. For every promoted item the only semantic lifecycle
change is `status: VALIDATED -> PROMOTED`; the item version, evidence,
applicability, scope, privacy, origin and lineage remain unchanged.

## N3 transition table

| knowledge_id | kind | status_before | promotion_readiness | authorization | evidence_refs | checkpoints | commits | scope_before | scope_after | origin_before | origin_after | status_after | result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `compress_occurrences_into_decisions` | `TASK_DECOMPOSITION_PATTERN` | `VALIDATED` | `PROMOTION_READY` | YES | `decision_units_1199`; `compress_occurrences_into_decisions_ui_ux_1_200_0_3` | `UI_UX_1_199`; `UI_UX_1_200` | `b407756`; `609d19f`; `dd7c154`; `82e913f` | `IA_CORE_BUILD` | `IA_CORE_BUILD` | `DEVELOPMENT_ORIGIN` | `DEVELOPMENT_ORIGIN` | `PROMOTED` | PASSED |
| `evidence_before_closure` | `VALIDATION_RULE` | `VALIDATED` | `PROMOTION_READY` | YES | `evidence_closure_1199`; `evidence_before_closure_ui_ux_1_200_0_3` | `UI_UX_1_194`; `UI_UX_1_199`; `UI_UX_1_200` | `d7321d2`; `7cb7134`; `b844511`; `c1bf467`; `1c9c0cd`; `d4e4913` | `IA_CORE_BUILD` | `IA_CORE_BUILD` | `DEVELOPMENT_ORIGIN` | `DEVELOPMENT_ORIGIN` | `PROMOTED` | PASSED |
| `focal_group_canonical_deep_test_policy` | `TEST_STRATEGY` | `VALIDATED` | `PROMOTION_READY` | YES | `test_policy_1199`; `focal_group_canonical_deep_test_policy_ui_ux_1_200_0_3` | `UI_UX_1_198`; `UI_UX_1_199`; `UI_UX_1_200` | `0784c38`; `dcb2aab`; `bf1f01c`; `b844511`; `d4e4913` | `IA_CORE_BUILD` | `IA_CORE_BUILD` | `DEVELOPMENT_ORIGIN` | `DEVELOPMENT_ORIGIN` | `PROMOTED` | PASSED |
| `preserve_contract_until_explicit_change` | `PRINCIPLE` | `VALIDATED` | `PROMOTION_READY` | YES | `preserve_contract_1199`; `preserve_contract_until_explicit_change_ui_ux_1_200_0_3` | `UI_UX_1_192`; `UI_UX_1_199`; `UI_UX_1_200` | `6ae13f4`; `7cb7134`; `bf1f01c`; `0d4ae4e` | `IA_CORE_BUILD` | `IA_CORE_BUILD` | `DEVELOPMENT_ORIGIN` | `DEVELOPMENT_ORIGIN` | `PROMOTED` | PASSED |
| `real_diff_over_planned_commit_name` | `COMMIT_STRATEGY` | `VALIDATED` | `PROMOTION_READY` | YES | `real_diff_commit_1197`; `real_diff_over_planned_commit_name_ui_ux_1_200_0_3` | `UI_UX_1_197`; `UI_UX_1_199`; `UI_UX_1_200` | `6b9c806`; `7cb7134`; `dd7c154`; `0d4ae4e`; `b844511`; `d4e4913` | `IA_CORE_BUILD` | `IA_CORE_BUILD` | `DEVELOPMENT_ORIGIN` | `DEVELOPMENT_ORIGIN` | `PROMOTED` | PASSED |
| `station_local_commits` | `COMMIT_STRATEGY` | `VALIDATED` | `PROMOTION_READY` | YES | `station_commits_1199`; `station_local_commits_ui_ux_1_200_0_3` | `UI_UX_1_199`; `UI_UX_1_200` | `48598d4`; `b407756`; `2ad648a`; `9248aae`; `609d19f`; `6b6b8d0`; `dd7c154`; `82e913f`; `0d4ae4e`; `bf1f01c`; `b844511`; `c1bf467`; `1c9c0cd` | `IA_CORE_BUILD` | `IA_CORE_BUILD` | `DEVELOPMENT_ORIGIN` | `DEVELOPMENT_ORIGIN` | `PROMOTED` | PASSED |
| `true_hard_frontier` | `STOP_CONDITION` | `VALIDATED` | `PROMOTION_READY` | YES | `hard_frontier_1199`; `true_hard_frontier_ui_ux_1_200_0_3` | `UI_UX_1_199`; `UI_UX_1_200` | `6b6b8d0`; `bf1f01c`; `d4e4913` | `IA_CORE_BUILD` | `IA_CORE_BUILD` | `DEVELOPMENT_ORIGIN` | `DEVELOPMENT_ORIGIN` | `PROMOTED` | PASSED |

The immutable promotion event is
`knowledge/global_operational/events/promotions/first_institutional_promotion_0_3.json`.

## Explicitly deferred and untouched inventory

`conditioned_autonomy`: `VALIDATED -> VALIDATED`; promotion executed: NO.
Reason: `DIRECTION_APPROVAL_REQUIRED` and Direction decision B requires more
evidence before promotion. It remains available only in modes that explicitly
allow `VALIDATED`.

The eight insufficient-evidence items remain `VALIDATED`:

```text
already_compliant_do_not_invent_change
compile_human_decisions_into_packages
contract_over_ui_inference
controlled_assembled_block_execution
internal_gates
local_rollback
no_fake_operational_state
no_giant_commit
```

The seven candidates remain `CANDIDATE`:

```text
apparent_frontier_can_be_designed_away
context_continuity_reduces_rework
cost_per_correctly_closed_surface
deterministic_distance_defines_block_size
human_intervention_is_high_value_resource
model_sufficiency_over_maximum_model
self_bootstrap
```

## Inventory and governance after N4

| measure | before | after |
|---|---:|---:|
| total items | 23 | 23 |
| PROMOTED | 0 | 7 |
| VALIDATED | 16 | 9 |
| CANDIDATE | 7 | 7 |
| OBSERVED | 0 | 0 |

`DEVELOPMENT_ORIGIN`, `IA_CORE_BUILD`, privacy classes, applicability,
evidence references, source history and lineage were preserved. Product/UI,
backend, payload, runtime, execution, providers, integrations, papers,
presets and agent memories were outside the change set.

The post-promotion governance recomputation is intentionally read-only over
the remaining `VALIDATED` records: `INSUFFICIENT_EVIDENCE = 8`,
`DIRECTION_APPROVAL_REQUIRED = 1`, `PROMOTION_READY = 0`, and
`PROMOTED = 0` in the new promotion set and `promoted_knowledge_ids = []`.
The seven promoted items are not reintroduced
as new promotion candidates.

The overlay-aware projection is persisted at
`knowledge/global_operational/assessments/promotion_assessment_post_gokv_0_3.json`.
The original post-UI/UX assessment remains unchanged.

`python -m gokv validate` passes with `valid = true`, 23 items and the exact
distribution above. Registry, item files and promotion event are consistent.

## N4 gate

`N4_GOKV_POST_PROMOTION_INTEGRITY_PASSED`.

No automatic promotion precedent was created. `PROMOTION_READY` remains an
eligibility result, not a lifecycle mutation. Future promotions still require
their own explicit authorization and valid transition.
