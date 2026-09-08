# UI/UX 1.198 - Microcopy contract surface map

## Gate

`N4_MICROCOPY_CONTRACT_SURFACE_MAP_PASSED`

N4 maps every N2 record and N3 classification to a surface and an evidence
anchor. The map does not treat visual proximity as proof of contract binding.
Its executable source is `contract_surface_maps()` in the N1 helper.

## Binding counts

| Binding type | Count | Meaning |
| --- | ---: | --- |
| `DIRECT_CONTRACT_BINDING` | 831 | Text is on a contract-aware surface and its meaning is evidenced by state/boundary vocabulary or classification. |
| `INDIRECT_CONTRACT_CONTEXT` | 159 | Context or source is contract-adjacent but does not alone prove a direct binding. |
| `PRESENTATIONAL_ONLY` | 130 | Surface presentation without a demonstrated authority or state binding. |
| `EDITORIAL_ONLY` | 408 | Editorial copy with no demonstrated contract relationship. |
| `UNKNOWN_BINDING` | 0 | No item is left without an owner/surface anchor. |
| `DIRECTION_REQUIRED_BINDING` | 96 | Evidence is insufficient to decide whether action/permission semantics are intended. |

The binding count sums to 1.624. `DIRECTION_REQUIRED_BINDING` is a hold state,
not a permission and not an implementation approval.

## Surface anchors

| Surface | Records | Contract anchor |
| --- | ---: | --- |
| `MASTER_SHELL_P0` | 72 | P0 |
| `P1_CONTRACT_OVERVIEW` | 90 | P1 / FSC-CO-01 / Contract Overview |
| `P1_BLOCKED_FORBIDDEN` | 61 | P1 / FSC-BF-02 / Blocked & Forbidden |
| `P1_VALIDATION_READINESS` | 100 | P1 / FSC-VR-03 / Validation & Readiness |
| `REQUEST_DRAFT_PANEL` | 167 | Request Draft Panel / FSC-RCP-04 |
| `P2_P3_MATRIX_CLOSURE` | 120 | P2 / P3 / Matriz P3 / closure evidence |
| `P2_P3_PANEL` | 430 | P2 / P3 detail panel |
| `CONTRACT_AWARE_WIDGETS` | 256 | widgets contract-aware |
| `NAVIGATION` | 24 | navigation / route reading |
| `I18N_CONTRACT_SURFACES` | 36 | i18n contract vocabulary |
| `I18N_GENERAL_UI` | 170 | i18n general UI |
| `ADMIN_PANELS` | 57 | administrative panels |
| `DOMAIN_ADMIN` | 41 | domain administration |

## Explicit contract mappings

The map records these anchors even when an individual item is editorial-only:

- **P0:** master shell state, `no_payload`, `not_available`, source/status and
  the no-runtime/no-execution boundary.
- **P1 / FSC-CO-01:** schema, source, status, fallback, readiness versus
  permission, allowed actions as declared data and forbidden actions as a
  visible boundary.
- **P1 / FSC-BF-02:** `blocked_capabilities`, `forbidden_actions`,
  deny-by-default, no-unlock/no-bypass/no-override and no operational CTA.
- **P1 / FSC-VR-03:** validation, readiness, warnings, errors, blockers and
  missing requirements as documentary states rather than live runtime.
- **Request Draft Panel / FSC-RCP-04:** draft/not-final,
  `DEFER_FINALIZATION`, no submit/send/dispatch/run/execute and no delivery.
- **P2/P3 and Matriz P3:** evidence/detail/closure copy remains secondary and
  cannot replace P0/P1 meanings.
- **Widgets contract-aware:** source, status, fallback, allowed actions,
  forbidden actions and blocked capabilities are read-only contract data.
- **CFG, `+` and DOMAIN:** affordance labels stay disabled/read-only; the map
  never turns them into actions.

## Field-level traceability

Every row has these fields:

`MICROCOPY_ID`, `surface`, `contract_anchor`, `binding_type`, `contract`,
`authority`, `payload_or_source`, `owner`, `state`, `risk`, `dependency` and
`future_change`.

The authority rule is explicit: backend contract remains authoritative; this UI
is read-only and deny-by-default. `allowed_actions` is declared data, not a
button. `forbidden_actions` and `blocked_capabilities` are visible limits, not
controls. Readiness and validation do not grant permission. `source`, `status`
and `fallback` remain evidence fields. `no_payload` and `not_available` remain
honest absence states.

## Contract vocabulary distribution

| Mapped evidence | Count |
| --- | ---: |
| `backend_internal_ui_payload.v1 / declared surface` | 667 |
| `blocked_capabilities / deny-by-default` | 68 |
| `readiness / validation (not permission)` | 67 |
| `source/status/fallback` | 67 |
| `source/status/fallback / not_available` | 50 |
| `backend_internal_ui_payload.v1 / no_payload` | 28 |
| `forbidden_actions (visible boundary, not a control)` | 39 |
| `allowed_actions (declared data, not a CTA)` | 27 |
| No demonstrated contract | 611 |

These are source-evidence counts, not claims that all nearby copy is
contractual. The map deliberately leaves 611 records without a demonstrated
contract binding while retaining their surface and source.

## N4 boundary

No product source was changed, no payload was created, no authority was moved,
and no UI text was renamed. A missing binding would be a documentation/test
failure, not a reason to invent one. N5 can now inspect geometry and visual
consistency with the correct surface context.
