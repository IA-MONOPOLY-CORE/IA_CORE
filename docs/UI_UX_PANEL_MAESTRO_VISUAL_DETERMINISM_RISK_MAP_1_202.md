# UI/UX 1.202 - Visual Determinism and Risk Map

## Gate

`N3_UI_UX_1_202_DETERMINISM_RISK_MAP_PASSED`

The map converts the terrain inventory into an executable boundary. The
current mission remains read-only. The next mission may act only on the two
measured responsive defects and their focused regression evidence.

## Deterministic route

| Unit | Route | Risk | Dependency | Product impact | Contract impact | Recommended action |
| --- | --- | --- | --- | --- | --- | --- |
| V-01 document containment | deterministic | low | browser matrix | none | none | preserve and guard |
| V-02 local containment | deterministic | low | intentional scroll containers | none | none | preserve and distinguish |
| V-04 breakpoint behavior | deterministic | low | existing media branches | none | none | preserve and test |
| V-05 readiness row | deterministic + preauthorized | medium | scoped CSS selector | CSS-only | none | fix wrapping locally |
| V-06 agents grid | deterministic + preauthorized | medium | legacy lower grid | CSS-only | none | fix mobile minimum locally |
| V-07 names/focus | deterministic | low | existing DOM and CSS | none | none | add guard only |
| V-13 browser metrics | deterministic + preauthorized | medium | static browser audit | test-only | none | add focused assertions |

P0, P1, P2/P3, matrix, widgets and Request Draft are already compliant and
remain preservation units, not work units.

## Classification

- `DETERMINISTIC`: measured containment, wrapping, accessible-name checks,
  viewport checks and focused regression assertions.
- `PREAUTHORIZED`: only the scoped CSS fixes for V-05/V-06 and tests/docs
  needed to prove them. The current mission does not apply them.
- `SELF_BOOTSTRAPPABLE`: six next-mission stations covering baseline, cascade
  evidence, the two responsive fixes, accessibility guard and checkpoint.
- `DIRECTION_REQUIRED`: none for the known measured fixes.
- `CONTRACT_OWNER_REQUIRED`: none in the known next block; required immediately
  if a proposal changes semantic wording, Level D, readiness, actions,
  permissions, HTML semantics, JS behavior or payload authority.
- `BLOCKED`: the hidden administrative/runtime-shaped lower surface is blocked
  from this visual block by the product boundary.
- `ALREADY_COMPLIANT`: nine inventory units, including global containment,
  focus/names, P0/P1/FSC, matrix, widgets and Request Draft.

## Apparent frontiers eliminated

The following are not hard frontiers for the selected block:

1. Choosing five browser sizes is specified by the current mission.
2. Measuring CSS behavior does not require changing CSS.
3. Adding a focused test does not require relaxing historical guards.
4. A CSS-only fix can be scoped to an existing selector without changing
   HTML, JS, i18n or contract fields.
5. The existing `PROMOTED_ONLY` pack is sufficient; no `VALIDATED` knowledge,
   new promotion or compiler change is required.
6. Local station commits and rollback are already specified by the inherited
   operational guidance.

## True hard frontier

`HARD_FRONTIER_STATION_INDEX = 7`.

The first real frontier is a semantic or contractual product decision: changing
Level D wording, readiness meaning, action/permission semantics, blocked or
forbidden meaning, HTML/ARIA semantics, JavaScript behavior, backend/payload
authority, runtime/execution, endpoint or integration behavior. A broad CSS
refactor also stops if it becomes a visual preference rather than a measured
containment correction.

At that point the owner is Direction/Contract Owner. The next mission must
stop before creating the diff and must not silently switch inheritance mode.

## Risk decisions

The next mission is allowed to use `ui/web/styles.css` only for V-05 and V-06,
with before/after viewport evidence and a local rollback. It may add tests,
fixtures, docs and GOKV capture. It may inspect `ui/web/index.html`, but may
not edit it. All other product surfaces remain protected.

No visual direction package is required for this block. The selected work is
derived from measured overflow, not from aesthetic preference.
