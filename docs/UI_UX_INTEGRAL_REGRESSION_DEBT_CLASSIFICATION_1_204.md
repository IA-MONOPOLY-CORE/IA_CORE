# UI/UX 1.204 - Integral Regression and Historical Debt Classification

## Gate

N4_UI_UX_1_204_REGRESSION_CLASSIFICATION_PASSED

## Test policy

The truth set is focal -> group -> canonical current -> deliberate historical
depth. A broad pytest invocation is not used as the sole truth because the
repository contains frozen checkpoint assertions and external provider tests.
No historical guard was weakened and no product file was changed to obtain
green.

## Regression matrix

| Layer | Command scope | Result | Interpretation |
| --- | --- | --- | --- |
| FOCAL | 1.204 contract/no-ghost, 1.204 visual, 1.203 focused hardening and 1.203 checkpoint | 13 passed | Current closure surfaces pass |
| GROUP | FOCAL plus 1.202 selection and GOKV promoted-only inheritance | 17 passed | Current continuity group passes |
| CANONICAL CURRENT | GROUP plus contract-aware, FSC, Validation & Readiness, Request Contract Preview, widgets and Request Draft guards; known frozen assertions excluded only for classification | 64 passed, 3 deselected | Current contract baseline passes |
| Historical probe | canonical candidates plus API/admin and older 1.175/1.178/1.190/1.200/1.201/1.146 guards | 62 passed, 8 expected historical failures, 4 deprecation warnings | No current or unknown failure |
| Deep historical inherited evidence | UI/UX 1.203 conditional deep probe | 90 passed, 15 expected snapshot mismatches | Already classified by 1.203; no guard relaxation |

## Historical failures classified

All eight failures were reproduced and assigned to an existing checkpoint
horizon. They are not current regressions:

| Historical assertion | Classification | Evidence | Product action |
| --- | --- | --- | --- |
| api admin identity expects CONTRACT-AWARE FRAMEWORK CONSOLE | OBSOLETE_TEST_EXPECTATION | Current UI intentionally uses IA_CORE // Contract-Aware HUD after commit 1d05260c; the older string belongs to the removed legacy identity | None in 1.204 |
| api admin provider test expects inline settings-fab handler | OBSOLETE_TEST_EXPECTATION | Inline handler was moved/blocked by the later panel hardening history; current contract controls are disabled and named | None in 1.204 |
| 1.200 exact CSS allowlist | HISTORICAL_CHECKPOINT_SNAPSHOT | 1.203 added the two authorized scoped responsive corrections after the 1.200 snapshot | Preserve 1.203 product; do not rewrite 1.200 |
| 1.201 productive-surface equality | HISTORICAL_CHECKPOINT_SNAPSHOT | 1.203 changed only the authorized stylesheet after the 1.201 horizon | Preserve 1.203 product; do not rewrite 1.201 |
| 1.175 current-scope guard | HISTORICAL_CHECKPOINT_SCOPE_GUARD | Guard freezes a 1.192 historical endpoint and does not understand later additive evidence | Keep assertion; classify by checkpoint |
| 1.178 current-scope guard | HISTORICAL_CHECKPOINT_SCOPE_GUARD | Same historical endpoint behavior | Keep assertion; classify by checkpoint |
| 1.190 current-scope guard | HISTORICAL_CHECKPOINT_SCOPE_GUARD | Same historical endpoint behavior | Keep assertion; classify by checkpoint |
| 1.146 read-only product equality | HISTORICAL_CHECKPOINT_SNAPSHOT | The product legitimately evolved after the 1.146 baseline; current baseline guards pass | Keep assertion; classify by checkpoint |

The separate canonical four-screen assertion that required the literal
attribute string class="four-screen-baseline-summary" was excluded from the
canonical current pass because the current equivalent class list is
class="four-screen-baseline-summary p0-command-summary". It is an
OBSOLETE_TEST_EXPECTATION from the 2026-08-29 guard, not a product defect.

## Debt categories

- CURRENT_REGRESSIONS: 0
- UNKNOWN_REGRESSIONS: 0
- BLOCKING_GAPS: 0
- CONTRACT_GHOSTS: 0
- HISTORICAL_DEBT_ITEMS: 8 reproduced failures plus the previously recorded
  15 deep snapshot mismatches.
- OBSOLETE_TEST_EXPECTATIONS: 3 (two admin/current-string assumptions and one
  literal class-order assumption).
- HISTORICAL_CHECKPOINT_SNAPSHOT: 3.
- HISTORICAL_CHECKPOINT_SCOPE_GUARD: 3.
- EXTERNAL_DEPENDENCY_ITEMS: 1 policy-excluded external Ollama integration
  suite; it is outside UI/UX and no failure was promoted into the current
  result.
- SUPERVISOR_COLLECTION_ISSUE: not reproduced in the 1.204 probe; no current
  collection blocker.
- NVIDIA HTTP 410/model retired: not found in the verified repository evidence;
  not counted.
- UNKNOWN: 0.

## Sanity

- New Python tests compile.
- Existing UI/UX contract guards pass in the canonical current set.
- No test adaptation touched product logic or removed an historical assertion.
- The expected failures are tied to old baselines or external dependencies,
  not to the current c2794799 contract-aware baseline.

## Gate conclusion

N4_UI_UX_1_204_REGRESSION_CLASSIFICATION_PASSED

The current line has no current regression and no unknown failure. Historical
debt remains visible and classified, so it cannot be mistaken for a green
current product claim.

