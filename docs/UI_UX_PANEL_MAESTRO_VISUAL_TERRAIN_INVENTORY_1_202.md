# UI/UX 1.202 - Visual Terrain Inventory

## Gate

`N2_UI_UX_1_202_VISUAL_TERRAIN_INVENTORY_PASSED`

Machine-readable source:
`tests/fixtures/ui_ux_1_202_visual_terrain_inventory.json`.

The inventory is based on the real HTML, the external stylesheet, the inline
style block and the five-viewport static browser audit. It does not infer a
defect from file size or rule count.

## Inventory totals

| Dimension | Count |
| --- | ---: |
| Total units inventoried | 14 |
| Already compliant | 9 |
| Deterministic fix | 2 |
| Deterministic refactor | 0 |
| Test gap | 1 |
| Documentation gap | 1 |
| Accessibility fix | 0 |
| Responsive fix | 2 |
| Visual direction required | 0 |
| Contract change required | 0 |
| Out of scope | 1 |

The classification counts are primary classifications. Responsive and
accessibility are orthogonal terrain dimensions and therefore can overlap the
primary classification.

## CSS cascade inventory

CSSOM observed 840 style rules across `ui/web/styles.css` and the inline style
block in `ui/web/index.html`. There are 103 rules inside media blocks and six
breakpoint conditions: 480, 620, 760, 980, 1080 and 1180 pixels. There are
105 repeated selector texts, 590 repeated normalized declaration strings and
28 `!important` declarations.

These are not automatic cleanup instructions. The repeated rules are a mix of
base rules, media overrides, visual-era scopes and the existing Request Draft
containment override. The next block may inspect computed styles and reduce a
selector only when a localized before/after regression guard proves that the
real cascade is preserved.

## Responsive findings

1. `Validation & Readiness` has one local non-wrapping state row that reaches
   231px inside a 195px grid block at `1280x800`. This is a deterministic,
   scoped wrapping/containment candidate.
2. `#agents-grid` retains a `minmax(300px, 1fr)` legacy minimum while its
   available track is 292px at `375x812`. This produces an 8px local overflow.
   It is a lower-console responsive candidate and not a contract failure.

Global horizontal overflow is zero at all required viewports. Request Draft
is inside the viewport at all required viewports, collapsing to a 44px tab on
mobile.

## Accessibility findings

No accessibility fix was selected. At each viewport there are 22 visible
controls, all with an accessible name, and zero enabled submit/reset controls.
Existing `:focus-visible` rules cover the read-only navigation, widgets,
matrix, Request Draft and utility controls. The disabled legacy forms are
protected boundary surfaces, not a reason to modify product in this mission.

## Contract and regression findings

P0, P1, P2/P3, the closure matrix, widgets and Request Draft remain
compliant. The four FSC, state markers, `no_payload`, `not_available`,
`pending`, `blocked`, `no-runtime`, `no-execution`, source/status/fallback and
deny-by-default remain intact.

The only test gap is a missing committed guard for the two local responsive
metrics. Historical guards and broad-suite debt remain separate and are not
relaxed. No HTML, JavaScript, i18n, backend, payload, runtime, execution,
endpoint or integration change is needed.

## Output

The natural next terrain is deterministic visual hardening of the two measured
responsive cases plus focused browser regression evidence. The current
mission does not implement that block.
