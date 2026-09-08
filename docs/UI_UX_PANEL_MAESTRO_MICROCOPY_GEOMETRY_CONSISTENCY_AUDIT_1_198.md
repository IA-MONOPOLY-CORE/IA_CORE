# UI/UX 1.198 - Microcopy geometry and consistency audit

## Gate

`N5_MICROCOPY_GEOMETRY_CONSISTENCY_AUDIT_PASSED`

N5 is browser evidence only. It observes the current product and records risks;
it does not change CSS, HTML, JavaScript, i18n, copy, state or contract.

## Browser session

| Field | Value |
| --- | --- |
| URL | `http://127.0.0.1:4173/index.html` |
| Page title | `IA_CORE // Panel Maestro / Documentary Shell` |
| Browser | Codex In-app Browser, read-only |
| Sessions | 1 |
| Viewports | 1440x1000, 1280x800, 768x1024, 390x844, 375x812 |
| Console | 0 warning/error entries in each viewport |
| Forms | 0 visible forms; no submitter observed |
| Product changes | 0 |

## Viewport evidence

`clientWidth` and `scrollWidth` are the document-level measurements. They are
equal in every viewport, so there is no global horizontal page overflow.
Item-level risks remain recorded below and are not silently normalized.

| Viewport | clientWidth | scrollWidth | body scrollWidth | Item overflow candidates | Long-wrap candidates | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1440x1000 | 1425 | 1425 | 1425 | 2 | 1 | `GEOMETRY_OK` + local `OVERFLOW_RISK` |
| 1280x800 | 1265 | 1265 | 1265 | 2 | 1 | `GEOMETRY_OK` + local `OVERFLOW_RISK` |
| 768x1024 | 753 | 753 | 753 | 0 | 1 | `GEOMETRY_OK` + `WRAP_RISK` |
| 390x844 | 375 | 375 | 375 | 1 | 1 | `GEOMETRY_OK` + local drawer `OVERFLOW_RISK` |
| 375x812 | 360 | 360 | 360 | 1 | 1 | `GEOMETRY_OK` + local drawer `OVERFLOW_RISK` |

## Observed geometry risks

The audit vocabulary remains closed: `GEOMETRY_OK`, `WRAP_RISK`,
`OVERFLOW_RISK`, `TRUNCATION_RISK`, `DENSITY_RISK`,
`SEMANTIC_VISUAL_AMBIGUITY` and `NO_ISSUE`. No truncation was observed in the
five passes; density and semantic-visual ambiguity remain candidate labels for
the relevant long or mixed-language records, not new product severities.

| Risk | Microcopy/surface | Evidence | Decision in 1.198 |
| --- | --- | --- | --- |
| `OVERFLOW_RISK` | `backend_internal_ui_payload.v1` and `backend_internal_ui_request.v1` values | Their `.layout-value` boxes reported local `scrollWidth > clientWidth` at 1440 and 1280; no document overflow or clipping occurred. | Record only; no CSS or wording fix. |
| `WRAP_RISK` | `Si no hay lista de detalle, el bloqueo sigue vigente; ausencia de lista no desbloquea.` | 3 lines at 1440, 4 at 1280, 5 at 768 and 3 at both mobile widths; no clipping. | Record only; wording is contract-sensitive. |
| `OVERFLOW_RISK` | `Contract request draft` / `#request-draft-panel` | At 390 and 375 the collapsed drawer geometry extends beyond the viewport (`horizontalClip=true`); the document itself remains width-contained. | Record as existing responsive drawer risk; no CSS or copy change. |
| `NO_ISSUE` | P0/P1 shell and key contract surfaces | Global width equality, visible shell, no console warnings/errors. | Keep current product unchanged. |

The mobile screenshot confirms the drawer is a collapsed side boundary rather
than a new CTA. It remains a geometry candidate for a later scoped responsive
decision, but N5 is not authorized to repair it.

## Surface checks

The browser observation found visible candidates in all required contract
surfaces: P0, Blocked & Forbidden, Validation & Readiness, Request Draft,
contract-aware widgets and the P2/P3 closure matrix. The current screen keeps
`NO RUNTIME / NO EXECUTION`, `BLOCKED_BY_CONTRACT`, `no_payload`,
`backend_internal_ui_payload.v1`, `allowed_actions`, `forbidden_actions` and
`blocked_capabilities` visible.

Controls observed in the 390x844 pass:

- flow and internal navigation buttons are read-only focus/navigation controls;
- local refresh controls carry `data-no-fetch`, `data-no-runtime` and
  `data-no-execution` boundaries;
- `CFG`, `+` and `DOMAIN` are disabled and contract-blocked;
- Request Draft toggle is read-only collapse/inspect behavior;
- Request Draft blocked control is disabled;
- no form and no `type=submit` control was observed;
- no new CTA, submit, dispatch, run, execute or permission affordance was
  created by this station.

## Consistency findings

The corpus contains 714 repeated text records. Repetition is not automatically
an error because the same value may be correct in different surfaces. N3 tags
145 as duplicate-equivalent and 569 as duplicate-contextual.

Observed consistency candidates for Direction review, without choosing a
replacement:

| Observation | Evidence | Risk |
| --- | --- | --- |
| Same state appears in token, sentence and badge forms | `readiness`, `READINESS`, `Readiness: no_payload`, `readiness / status` | `CONSISTENCY_CANDIDATE`; may be exact contract vocabulary. |
| English and Spanish are mixed in the same contract surfaces | `Contract Overview`, `Blocked & Forbidden`, `Validation & Readiness`, `Request contract`, `Readiness`, `Schema`, `Next Step` alongside Spanish explanatory copy | `AMBIGUOUS_REQUIRES_DIRECTION`; translation is not assumed safe. |
| Casing and separator variants exist | `passed`, `PASSED`, `PASSED_WITH_MINOR_DEBT`, `warnings / errors`, `warning/error` | `CONSISTENCY_CANDIDATE`; casing may be a state token. |
| Fallbacks repeat across surfaces | `no_payload` and `not_available` occur in badges, detail rows, widgets and i18n | `DUPLICATE_CONTEXTUAL`; do not merge context. |
| Action language appears inside anti-action explanations | `run`, `execute`, `dispatch`, `submit`, `allowed_actions`, `forbidden_actions` | `ACTION_PERMISSION_SENSITIVE`; do not rewrite as a CTA or permission. |

No contradictory wording was auto-resolved. A contradiction would need source,
state and contract evidence plus Direction; visual proximity is insufficient.

## N5 gate evidence

The focal test freezes the five viewport results, the browser evidence fields,
the geometry risk vocabulary, the read-only/no-submit boundary and the
protected product baseline. The audit is an input to N6; it does not authorize
N7 wording work.
