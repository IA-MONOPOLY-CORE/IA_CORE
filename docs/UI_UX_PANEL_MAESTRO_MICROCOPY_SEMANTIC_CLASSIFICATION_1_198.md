# UI/UX 1.198 - Semantic classification of the microcopy corpus

## Gate

`N3_MICROCOPY_SEMANTIC_CLASSIFICATION_PASSED`

N3 classifies the N2 records without changing their text. The classification is
conservative: when a term can affect state, readiness, permission, action,
authority or the meaning of a boundary, the record is raised to a higher risk
or marked for Direction. No category below authorizes an edit.

## Primary classification counts

| Classification | Count | Direction needed | Exactness |
| --- | ---: | ---: | ---: |
| `EDITORIAL_SAFE` | 408 | No | No |
| `CONTRACTUAL_EXACT` | 556 | Yes | Yes |
| `CONTRACTUAL_EXPLANATORY` | 93 | Yes | No |
| `STATE_LABEL` | 4 | Yes | No |
| `READINESS_LABEL` | 58 | Yes | Yes |
| `PERMISSION_SENSITIVE` | 0 | Yes | Yes |
| `ACTION_SENSITIVE` | 15 | Yes | No |
| `BLOCKER` | 138 | Yes | Yes |
| `WARNING` | 27 | Yes | No |
| `ERROR` | 19 | Yes | No |
| `FALLBACK` | 10 | Yes | Yes |
| `NO_PAYLOAD` | 31 | Yes | Yes |
| `NOT_AVAILABLE` | 52 | Yes | Yes |
| `NAVIGATION` | 14 | No | No |
| `FORM_LABEL` | 42 | No | No |
| `PLACEHOLDER` | 20 | No | No |
| `ACCESSIBILITY_COPY` | 41 | Yes | No |
| `LEGACY_ACTIVE` | 0 | Yes | No |
| `LEGACY_INACTIVE` | 0 | Yes | No |
| `AMBIGUOUS_REQUIRES_DIRECTION` | 96 | Yes | No |
| `UNKNOWN_REQUIRES_DIRECTION` | 0 | Yes | No |

The sum is 1.624 primary classifications. `PERMISSION_SENSITIVE` remains zero
because this deterministic pass does not invent a permission interpretation;
the 96 ambiguous records are the correct holding category when action-like or
permission-like language lacks enough evidence.

## Risk levels

| Risk | Count | Interpretation |
| --- | ---: | --- |
| `RISK_0_EDITORIAL` | 398 | Editorial copy with no demonstrated contract impact |
| `RISK_1_PRESENTATIONAL` | 66 | Presentational or density-sensitive copy |
| `RISK_2_CONTRACT_ADJACENT` | 65 | Accessible, form or legacy context near a contract surface |
| `RISK_3_CONTRACT_SENSITIVE` | 984 | State, blocker, fallback, warning, error or contract vocabulary |
| `RISK_4_DIRECTION_REQUIRED` | 111 | Action/permission-like ambiguity or an explicit Direction boundary |

Risk is intentionally not a priority or permission. It is a change-sensitivity
signal. A high-risk item can be kept exactly as-is, and a low-risk item still
cannot be edited in 1.198.

## Duplicate tags

Duplicate classification is a secondary tag so it does not erase semantic
meaning:

- `DUPLICATE_EQUIVALENT`: 145 records share exact text, surface and initial
  type with another record.
- `DUPLICATE_CONTEXTUAL`: 569 records share text while differing by surface or
  initial context.
- `NONE`: 910 records have no exact text duplicate.

Repeated `blocked`, `no_payload`, `not_available`, readiness, warning and label
values therefore remain independently traceable. No automatic harmonization is
proposed.

## Per-record decision fields

For every N2 `MICROCOPY_ID`, N3 records:

`classification`, `duplicate_classification`, `reason`, `risk`,
`future_change`, `decision_owner`, `contract_touched`, `automatable`,
`direction_required`, and `must_remain_exact`.

The deterministic owners are `UI_EDITORIAL_OWNER`, `ACCESSIBILITY_OWNER`,
`CONTRACT_OWNER` and `DIRECTION`. A `DIRECTION` owner is a stop boundary, not a
delegation to the agent.

## Interpretation rules

1. `no_payload`, `not_available`, `blocked`, `forbidden`, readiness,
   validation, warnings and errors are treated as contract-sensitive evidence.
2. Action-like and permission-like vocabulary is not rewritten into a safer
   phrase. It is either kept in its demonstrated category or placed in
   `AMBIGUOUS_REQUIRES_DIRECTION`.
3. Accessible names are not assumed to be interchangeable with visible labels.
4. Duplicate values are not deduplicated away.
5. Legacy status is not inferred from age or naming; only an explicit legacy
   marker can set the legacy fields.
6. No record receives a new state, severity, action or permission.

## Examples of conservative classification

| Existing record shape | Classification | Why no edit is made |
| --- | --- | --- |
| `READINESS: no_payload` | `NO_PAYLOAD` | It declares absence, not permission or availability. |
| `blocked_by_contract` | `BLOCKER` | It is a hard boundary and must not become an affordance. |
| `Bloqueado por contrato` in an execute slot | `CONTRACTUAL_EXACT` | Context ties it to the contract boundary. |
| `run`, `execute`, `dispatch`, `submit` without enough context | `AMBIGUOUS_REQUIRES_DIRECTION` | The source does not prove label versus action semantics. |
| A repeated `not_available` in two surfaces | `NOT_AVAILABLE` plus duplicate tag | Context is retained; no harmonization is inferred. |

## Gate evidence

The focal test verifies one primary classification per inventory record, allowed
categories and risk levels, exact counts, duplicate preservation, conservative
Direction flags, the N2 digest and the protected product baseline. N3 changes
only documentation/tests. N4 can now map these classifications to their
contract surfaces.
