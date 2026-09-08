# UI/UX 1.201 - Microcopy Direction Closure Audit

## Gate

`N2_UI_UX_1_201_DIRECTION_CLOSURE_AUDIT_PASSED`

La auditoría revalidó el allowlist machine-readable de UI/UX 1.200, la
integridad del diff real y las ocho decisiones de Dirección. No se reabrió
microcopy ni se convirtió una preferencia editorial en una decisión nueva.

## Decision closure

| Decisión | Resultado verificado | Conteo / evidencia |
| --- | --- | --- |
| D1 = B | Patrón editorial scoped; el copy vigente ya era conforme | 295 candidatos, 295 `ALREADY_COMPLIANT`, wording real 0 |
| D2 = A | Cada contexto y unidad permanecen separados | 194 `KEEP_CONTEXTUAL` de consistencia; sin canonización global |
| D3 = B | Geometría únicamente sobre riesgos demostrados | 15 `ALLOWED_GEOMETRY_CHANGE`; CSS real, un bloque scoped |
| D4 = A | Variantes contextuales preservadas | 36 variantes contextuales, sin merge semántico |
| D5 = A | Blockers, warnings, límites, errores y evidencia contract-sensitive intactos | 139 `KEEP_CONTRACT` |
| D6 = A | Acción y permiso siguen read-only | 15 `KEEP_ACTION_PERMISSION`; sin CTA, submit ni permiso |
| D7 = A | Rol ambiguo no reinterpretado | 38 `KEEP_AMBIGUOUS_ROLE` |
| D8 = A | Vocabulario contractual Level D intacto | 692 `KEEP_LEVEL_D` |

La diferencia entre “candidato editorial” y “cambio realizado” es
intencional: el allowlist conserva la posibilidad autorizada, mientras que
Git demuestra que `ui/web/index.html` no cambió. Por eso el resultado efectivo
de los 295 es `ALREADY_COMPLIANT` y el wording delta es `0`.

## Unresolved ledger

| Campo | Resultado |
| --- | ---: |
| `UNRESOLVED_DIRECTION_PACKAGES` | 0 |
| `UNRESOLVED_DECISION_UNITS` | 0 |
| `UNMAPPED_MICROCOPY` | 0 |
| `ACCIDENTAL_CONTRACT_CHANGE` | 0 |
| `ACCIDENTAL_WIDENING` | 0 |

Los ocho packages de Dirección están presentes en el allowlist; cada item
tiene `microcopy_id`, `decision_unit_id`, superficie y autoridad. Las
superficies HTML, i18n, backend y payload no tienen diff entre `4618c59` y el
cierre de 1.200. El único cambio productivo histórico continúa siendo el
bloque CSS de geometría auditado en N1.

## Estado de fase

`MICROCOPY_DIRECTION_DECISIONS = CLOSED`

La fase queda cerrada porque sus decisiones tienen resultado observable, los
295 potenciales no generaron wording, las 15 correcciones geométricas están
limitadas al allowlist, las 692 ocurrencias Level D siguen intactas y no hay
ledger residual. La siguiente misión no debe seguir editando microcopy por
inercia.
