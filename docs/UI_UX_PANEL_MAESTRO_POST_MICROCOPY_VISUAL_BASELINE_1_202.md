# UI/UX 1.202 - Post-Microcopy Visual Baseline Audit

## Gate

`N1_UI_UX_1_202_VISUAL_BASELINE_AUDIT_PASSED`

This is a read-only baseline. No product file was edited. The page was served
from `ui/web` with a static HTTP server only; FastAPI, Supervisor, backend
endpoints, runtime and execution were not started.

Baseline commit: `2555a7fe`.

## Browser matrix

| Viewport | document client/scroll | horizontal overflow | console errors/warnings | Request Draft | result |
| --- | ---: | ---: | ---: | --- | --- |
| 1440x1000 | 1425 / 1425 | 0 | 0 | 340px, inside viewport | PASS |
| 1280x800 | 1265 / 1265 | 0 | 0 | 340px, inside viewport | PASS with local row debt |
| 768x1024 | 753 / 753 | 0 | 0 | 340px, inside viewport | PASS |
| 390x844 | 375 / 375 | 0 | 0 | collapsed 44px, inside viewport | PASS |
| 375x812 | 360 / 360 | 0 | 0 | collapsed 44px, inside viewport | PASS with legacy grid debt |

The page scrollbar is vertical and expected. No accidental document-level
horizontal overflow was observed.

## Contract surfaces preserved

- Four contract screens remain present: `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03`
  and `FSC-RCP-04`.
- P0 remains visible with five route zones.
- P1 remains visible with the four-screen route and its contractual stages.
- The closure matrix remains visible with 20 rows and 26 badges.
- Four contract-aware widgets remain present.
- Request Draft remains a collapsed/expanded read-only preview, not a CTA.
- `no_payload`, `not_available`, `pending`, `blocked`, `no-runtime` and
  `no-execution` remain documentary states.

## Accessibility and interaction boundary

The effective visible-control audit was repeated at all five viewports:

- 22 visible controls at every viewport;
- 0 unnamed visible controls;
- 0 enabled submit/reset controls;
- disabled contractual controls remain disabled;
- focus-visible rules exist for the read-only navigation, widgets, matrix,
  Request Draft and utility controls.

The page contains one legacy form and a disabled legacy submit control, but no
enabled submitter is visible or operational in this read-only surface.

## Findings

### `VISUAL_DEFECT`

1. At `1280x800`, one `validation-readiness-block` is narrower than its
   non-wrapping state row. The row reaches `231px` while its block is `195px`.
   The document itself does not overflow, but the local row can exceed its
   grid track. This is a deterministic responsive fix candidate.
2. At `375x812`, the legacy `#agents-grid` keeps a `minmax(300px, 1fr)` track
   while the available track is `292px`, producing an 8px local overflow.
   This is a deterministic responsive fix candidate in the lower legacy
   surface, not a contract or runtime defect.

### `ALREADY_COMPLIANT`

Global containment, Request Draft containment, visible accessible names,
focus affordances, P0/P1/FSC preservation, widgets, matrix, state semantics,
no-submit boundary and console cleanliness are compliant across the matrix.

### `DEBT`

The CSS is historically layered between `ui/web/styles.css` and the inline
style block in `ui/web/index.html`. CSSOM reports 840 style rules, 103 rules
inside media blocks, 105 repeated selector texts and 28 `!important`
declarations. These counts are inventory signals, not permission to delete or
merge rules. The next mission must use computed behavior and scoped diffs.

### `TEST_ONLY_DEBT`

There is no committed browser-metric guard for the two local responsive cases
identified above. Historical broad-suite failures remain outside this gate and
must not be relaxed here.

### `HISTORICAL_GUARD_DEBT`

The known 1.196-1.201 historical guards remain a separate concern. This audit
does not change them and does not treat their stale baselines as product
regressions.

### `CONTRACTUAL_FRONTIERS`

Changing wording, readiness meaning, action or permission semantics, HTML
structure, JavaScript behavior, i18n, backend, payload, runtime, execution,
endpoint, integration or Level D crosses the contract boundary. No such
change is needed to address the two measured responsive cases.

## Classification rule

The two local overflows are recorded for the next block; they are not fixed in
1.202. This mission remains read-only and closes with an empty product diff.
