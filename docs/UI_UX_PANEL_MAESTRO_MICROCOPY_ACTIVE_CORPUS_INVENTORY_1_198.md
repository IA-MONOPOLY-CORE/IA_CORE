# UI/UX 1.198 - Active microcopy corpus inventory

## Gate

`N2_ACTIVE_MICROCOPY_CORPUS_INVENTORY_PASSED`

The inventory is a complete, non-deduplicated snapshot of the current active
or potentially visible corpus. It is generated from the exact N1 registry by
`tests/ui_ux_panel_maestro_microcopy_1_198_support.py`. N2 does not edit HTML,
CSS, JavaScript, i18n, backend or payload.

## Snapshot identity

| Field | Value |
| --- | --- |
| Baseline | `6b9c806` |
| Total corpus items | `1624` |
| Corpus digest | `4e5e84fbfa63aeb257813536febf91b2fc73b99e0384340b4194609ba48201ff` |
| Product changes | `0` |
| Deduplication | None; repeated text keeps its surface context |
| Active wording changes | `0` |

The digest includes every record and every field. It is not a digest of unique
strings, so a duplicated fallback, badge, label or warning remains separately
traceable.

## Counts

| Measure | Count | Meaning |
| --- | ---: | --- |
| `TOTAL_CORPUS_ITEMS` | 1624 | All materialized records |
| `HTML_ITEMS` | 1084 | Direct text plus accessible attributes |
| `HTML_TEXT_ITEMS` | 1032 | Direct visible/potential text nodes |
| `HTML_ATTRIBUTE_ITEMS` | 52 | `aria-label`, `title`, `placeholder`, `alt` |
| `I18N_ITEMS` | 217 | Flattened string leaves with exact keys |
| `JS_ITEMS` | 323 | Potentially renderable string literals |
| `STATE_ITEMS` | 219 | Blocker, readiness or exact contract-like state records |
| `WARNING_ITEMS` | 27 | Warning/advertencia records |
| `ERROR_ITEMS` | 19 | Error/failed records |
| `FALLBACK_ITEMS` | 93 | Fallback, `no_payload` and `not_available` records |
| `EDITORIAL_ITEMS` | 1225 | Initial editorial-safe classification; N3 may raise risk |
| `UNKNOWN_ITEMS` | 0 | No unlocated surface; semantic ambiguity is handled in N3 |
| `ACCESSIBILITY_ITEMS` | 41 | Explicit accessible-copy records |
| `DUPLICATE_ITEMS` | 714 | Repeated text values retaining context |
| `CONTRACT_AWARE_ITEMS` | 1079 | Initial surface/term signal, not a final binding decision |
| `WRAP_RISK_ITEMS` | 48 | Preliminary long-copy wrapping signal |
| `DENSITY_RISK_ITEMS` | 94 | Preliminary medium-long density signal |

## Record schema

Every record has all of the following fields:

`MICROCOPY_ID`, exact current `text`, `source`, `file`, `location`, `surface`,
`visibility`, `language`, `initial_type`, `contract_aware`, `active`,
`legacy`, `potential_duplicate`, `wrapping_risk`, `semantic_risk`.

The ID families are stable and preserve source order:

| Family | Coverage |
| --- | --- |
| `HTML_TEXT_NNNN` | Every direct text node outside script/style/noscript |
| `HTML_ATTR_NNNN` | Every non-empty `aria-label`, `title`, `placeholder` and `alt` |
| `I18N_NNNN_<key>` | Every string leaf in `i18n_es.json` |
| `JS_<SOURCE>_<LINE>_<ORDINAL>` | Every textual or contract-signaling JS literal selected as potentially renderable |

## Source inventory

### HTML direct text and attributes

The HTML inventory covers the master shell, P0 state, P1 Contract Overview,
P1 Blocked & Forbidden, P1 Validation & Readiness, Request Draft Panel,
P2/P3 closure matrix, navigation, widgets, badges, disabled controls and
legacy active text. Direct examples include `NO RUNTIME / NO EXECUTION`,
`READINESS: no_payload`, `blocked_by_contract`, `Validation & Readiness`,
`allowed_actions`, `forbidden_actions`, `blocked_capabilities` and the
non-operational Request Draft explanations. Accessible attributes remain
records instead of being merged with visible text.

### i18n

All 217 string leaves are inventoried by exact key, including common controls,
status values, readiness/validation copy, fallbacks, warnings/errors,
Request contract wording, administrative copy, placeholders and provider or
domain messages. A key is never inferred from its value and an unknown key is
rejected by the N1 guard.

Representative keys retained as exact records:

| Key | Current value | Initial surface |
| --- | --- | --- |
| `status.no_payload` | `no_payload` | I18N_CONTRACT_SURFACES |
| `status.not_available` | `not_available` | I18N_CONTRACT_SURFACES |
| `interaction_model.contract_block` | `Bloqueado es un límite contractual.` | I18N_CONTRACT_SURFACES |
| `debate.task_placeholder` | `Draft local; requiere backend_internal_ui_request.v1 y allowed_actions.` | I18N_CONTRACT_SURFACES |
| `orchestration.execute` | `Bloqueado por contrato` | I18N_CONTRACT_SURFACES |
| `providers.catalog_pending` | `El backend todavía no publicó el catálogo de proveedores.` | I18N_GENERAL_UI |

### JavaScript

The JS inventory is intentionally filtered to renderable-looking literals or
contract-signaling tokens. It covers contract-aware widgets, admin panels,
console/request-draft interactions and domains. Identifiers, URLs and module
syntax are not falsely reported as microcopy. A literal is still marked
`POTENTIAL_VISIBLE` because source inspection alone cannot prove runtime
visibility for every branch.

## Surface coverage

The materialized surfaces are `MASTER_SHELL_P0`, `P1_CONTRACT_OVERVIEW`,
`P1_BLOCKED_FORBIDDEN`, `P1_VALIDATION_READINESS`, `REQUEST_DRAFT_PANEL`,
`P2_P3_MATRIX_CLOSURE`, `CONTRACT_AWARE_WIDGETS`, `NAVIGATION`,
`DOMAIN_ADMIN`, `ADMIN_PANELS`, `I18N_CONTRACT_SURFACES` and
`I18N_GENERAL_UI`. No record is discarded merely because its text repeats.

The counts are inventory facts, not semantic approvals. A record can be
initially editorial-safe and still become `RISK_3` or `RISK_4` in N3 when its
surface or wording suggests state, authority, readiness, permission or action.

## N2 gate evidence

The focal test verifies the exact count set, complete record schema, stable IDs,
source registry, corpus digest, protected product baseline and representative
coverage for HTML, i18n, JS, states, warnings, errors, fallbacks, disabled
copy, accessible copy and contract-aware surfaces. No active wording was
changed. The next station is classification, not copy editing.
