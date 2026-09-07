# UI/UX Panel Maestro - Request Draft Panel Visual Demotion 1.189

## Scope and input

- Base verified: `72b6f71` on `main`, synchronized with `origin/main` before the intervention.
- Previous decision: `UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_MATRIX_CHECKPOINT`.
- Previous readiness: `ready_for_ui_ux_1_189_selected_visual_block_implementation`.
- Selected candidate: **Candidate A - Request Contract Preview / Request Draft Panel**.
- This is a surgical visual implementation. It does not add active UI, submit, dispatch, runtime, execution, endpoints, integrations, backend changes, payload v2, P0, P1, Matrix changes, P3 changes, widgets contract-aware changes, or i18n changes.

## Existing contract preserved

The panel remains a secondary, visible, legible desktop panel and mobile drawer. Its existing `read-only`, `blocked`, disabled, `aria-readonly`, `aria-expanded`, `aria-controls`, `no submit`, `no dispatch`, `no execution`, `no-runtime`, `no-execution`, deny-by-default and disabled behavior remain unchanged. The supported contract remains `backend_internal_ui_payload.v1`; payload v2 is absent.

No HTML, contractual JavaScript, `backend-contract-widgets.js`, `console-interactions.js`, `admin-panels.js`, `domains.js`, i18n, backend, endpoints, payloads, integrations, runtime or execution code was edited.

## CSS-only visual demotion

`ui/web/styles.css` now scopes the visual change to `body #request-draft-panel.request-draft-panel` and its existing child selectors. It replaces the critical red edge/glow with a restrained slate edge and quiet surface, tones down the draft textarea and guidance, keeps the lock line readable, and changes the disabled blocked control from cyan-gradient CTA language to a neutral disabled state.

The CSS does not hide the panel, use `display: none`, use `visibility: hidden`, reduce its desktop width, modify its collapse transform, add pointer affordance to the blocked control, or create an operational action. The existing mobile drawer breakpoint is preserved with only modest padding and gap refinement.

## Validation and limitations

Static contract and diff guards verify the panel structure, existing disabled/ARIA markers, v1-only payload surface, absence of new operational state, the scoped CSS selectors, no global panel hiding, no desktop `display: none`, no hidden visibility, and no new primary CTA styling for the blocked control. The historical UI/UX 1.175 through 1.188 guards receive additive allowlist continuity only.

A local server was started for visual review at `http://localhost:8770/`; desktop `1440x1000`, mobile `390x844`, and live resize verification could not be captured because the supplied browser-control runtime exited before creating a tab with `windows sandbox failed: helper_unknown_error: setup refresh had errors`. This is an environment limitation, not an application error. The CSS preserves the existing 340 px desktop panel and existing mobile drawer geometry by design; visual runtime capture remains a follow-up verification item.

## Result

`UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_PASSED`

Readiness: `ready_for_ui_ux_1_190_request_draft_panel_visual_demotion_checkpoint`

Next prompt exact: `PROMPT UI/UX 1.190 — Checkpoint de democión visual del Request Draft Panel del Panel Maestro IA_CORE contract-aware`

UI/UX 1.190 was not executed by this intervention.

## Recommendation

Use an advanced stable model with browser inspection and focused repository tests at high effort for the checkpoint. The recommendation is harmonic: it does not seek the minimum or maximum model, tool, or effort level. Raise effort only if visual geometry, readonly contract markers, desktop/mobile drawer behavior, P0/P1, Matriz, or widget evidence becomes ambiguous; lower it only for documentation-only corrections. Rework risk is low because the implementation is CSS-only and the contractual surface is untouched.

## Evidencia de recomendación

No backend, no endpoints y no integrations fueron modificados. La recomendación de modelo, herramienta y nivel de esfuerzo no busca el mínimo ni el máximo: prioriza balance verificable del contrato read-only.
La recomendacion no busca el minimo y no busca el maximo.
