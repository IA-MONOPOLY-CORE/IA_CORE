# UI/UX 1.204 - Integral Visual / Responsive / Accessibility Audit

## Gate

N3_UI_UX_1_204_VISUAL_RESPONSIVE_ACCESSIBILITY_AUDIT_PASSED

## Boundary

Dirección decidió B: preservar el baseline actual. Esta estación verifica el
baseline final y no introduce preferencia visual, CSS, HTML, ARIA ni
interacción nueva.

The five-viewport matrix was checked against the live static surface served from
ui/web. The browser remained static-only: backend, FastAPI, supervisor,
endpoints, runtime and execution were not started.

## Matrix

| Viewport | Global client/scroll | Source block | Source row | Agents grid | Request Draft | Widgets | Controls | Unnamed | Active submitters |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1440x1000 | 1425/1425 | 235/235 | 207/207 | 1025/1025 | 1424.8 right, 340px expanded, inside | 4 / 0 local overflow | 24 | 0 | 0 |
| 1280x800 | 1265/1265 | 195/195 | 167/167 | 865/865 | 1264.8 right, 340px expanded, inside | 4 / 0 local overflow | 24 | 0 | 0 |
| 768x1024 | 753/753 | 302/302 | 274/274 | 659/659 | 752.8 right, 340px expanded, inside | 4 / 0 local overflow | 24 | 0 | 0 |
| 390x844 | 375/375 | 276/276 | 248/248 | 307/307 | 374.2 right, 44px collapsed tab, inside | 4 / 0 local overflow | 22 | 0 | 0 |
| 375x812 | 360/360 | 261/261 | 233/233 | 292/292 | 359 right, 44px collapsed tab, inside | 4 / 0 local overflow | 22 | 0 | 0 |

The normalized global comparison uses the document client width after the browser
scrollbar is accounted for. All global and scoped overflows are zero.

Machine-readable evidence:
tests/fixtures/ui_ux_1_204_visual_accessibility_matrix.json

## Visual checks

- global overflow: 0 on all five viewports;
- accidental local overflow: 0 for Validation & Readiness source block and
  row, agents grid, widgets and Request Draft;
- Request Draft remains inside the viewport and changes to the existing compact
  mobile tab;
- the four contract-aware widgets remain visible and legible;
- the Matriz remains usable and secondary;
- P0/P1 hierarchy remains legible;
- desktop, tablet and mobile readability remain within the already accepted
  baseline;
- no new CSS, HTML, copy or state was introduced.

## Accessibility checks

- visible controls have accessible names: 24 desktop/tablet and 22 mobile,
  unnamed controls 0;
- active submitters: 0 at every viewport;
- contract-aware screens retain aria-labelledby/aria-describedby relationships;
- existing focus-visible rules remain present for widgets, Matriz, Request Draft
  toggle and console utilities;
- Request Draft toggle retains a name and title: Abrir vista previa del draft
  bloqueado;
- scoped contract surfaces contain no form and no enabled submitter;
- the pre-existing administrative domain form remains disabled by contract and
  is outside the FSC read-only scope;
- no operational form, keyboard route or action boundary was added.

## Console and runtime

The accepted 1.203 browser run recorded zero console errors and zero unexpected
console warnings. 1.204 changes no HTML, JavaScript or CSS, and the static
recheck produced the same surface and metrics. No backend, endpoint, runtime,
execution or integration was started.

## Gate conclusion

N3_UI_UX_1_204_VISUAL_RESPONSIVE_ACCESSIBILITY_AUDIT_PASSED

No visual, responsive or accessibility blocker is present in the current
baseline. The visual baseline is preserved, not expanded.

