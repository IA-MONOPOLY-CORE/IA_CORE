# GOKV Promotion Governance v1

## Gate

`N4_GOKV_PROMOTION_GOVERNANCE_PASSED`

## Policy

`gokv.promotion_policy.v1` assesses lifecycle state without changing it. Automatic promotion is explicitly disabled.

An item can be considered `PROMOTION_READY` only when the assessment finds:

- at least two evidence references;
- at least two source checkpoints showing repetition;
- at least two independent source commits;
- no known contradictory lineage;
- declared scope and applicability;
- reviewed exceptions;
- `HIGH` confidence;
- current freshness;
- declared source quality;
- current contract compatibility;
- a reversible reuse path.

The policy also recognizes:

- `VALIDATED_NOT_PROMOTION_READY`;
- `DIRECTION_APPROVAL_REQUIRED` for institutional autonomy, model, cost, or architecture direction;
- `INSUFFICIENT_EVIDENCE`;
- `CONFLICTING_EVIDENCE`.

## Generation 0 Assessment

All 16 `VALIDATED` items are assessed. Each currently has one evidence reference, so each is `INSUFFICIENT_EVIDENCE`. This is a policy result, not a defect and not a rejection of the knowledge. The items remain available through explicit `DEVELOPMENT_VALIDATED` compilation.

No item is promoted. The machine-readable assessment is stored at `knowledge/global_operational/assessments/promotion_assessment_v1.json` and contains one decision per validated item with evidence, criteria, risk, reasoning summary, blockers, and recommendation.

## Safety

Assessment never mutates lifecycle state, creates authority, changes scope, rewrites evidence, or overrides current contracts. Any future promotion requires a separate explicit transition after the policy result and, where applicable, direction approval.
